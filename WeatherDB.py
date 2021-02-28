import requests
import json
import sqlite3
import os

#connecting to the data base and creating a local db
db = sqlite3.connect('local.db')
cur = db.cursor()

#sending get Request to weatherstack weather api
def getRequestToWheaterApi(city,unit):
  params = {}
  params['access_key'] = '35f94c9e0225a1ecf14595d7b0d1bcef'
  params['query'] = city
  params['unit'] = unit
  api_result = requests.get('http://api.weatherstack.com/current', params)
  if not os.path.exists(os.path.dirname('JSON_files/')):
      os.makedirs(os.path.dirname('JSON_files/'))
  filePath = 'JSON_files/'+city+'_Weather_Info.json'    
  writeFile = open(filePath, 'w')     
  writeFile.write(api_result.text)
  writeFile.close()
  return filePath

#loading the local JSON file we got from the get Request to the weatherstack api
def loadWeatherDatatoSqlite3(res):
  with open(res) as f:
    api_response = json.load(f)
  return api_response

#inserting the values to the table in the local data base
def insertIntoTable(data,tableName,cur):
  values = [int(x) if isinstance(x, bool) else x for x in data.values()]
  columns = ', '.join(data.keys())
  placeholders = ', '.join('?' * len(data))
  sql = 'INSERT INTO '+tableName+' ({}) VALUES ({})'.format(columns,placeholders)
  values_ofReq = [int(x) if isinstance(x, bool) else x for x in values]
  cur.execute(sql, values_ofReq)

#creating the request table, each request that sents to the weather api insreted to this table
def createReqTable(api_response,cur):
  cur.execute('''CREATE TABLE IF NOT EXISTS Requests(
                  request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  type text, query TEXT, 
                  language TEXT,unit TEXT)''')
   
  request_data = api_response["request"] 
  insertIntoTable(request_data,'Requests',cur)
  

#creating the Location table,for each request that sents to the weather api we insert that location data to this table
def createLocationTable(api_response,cur):  
  cur.execute('''CREATE TABLE IF NOT EXISTS Locations(
                  request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name text, country TEXT, 
                  region TEXT,lat REAL,lon REAL,timezone_id TEXT,localtime DATETIME, 
                  localtime_epoch INTEGER,utc_offset REAL)''')
  location_data = api_response["location"]
  insertIntoTable(location_data,'Locations',cur)

#SQLite does not support arrays so this function flatting an array of strings by concatenation each string on it
def flatt(data,key):
  toFlatt = data[key]
  updated = ', '.join(toFlatt)
  data[key] = updated

#creating the Current table,for each request that sents to the weather api we insert that current weather data to this table
def createCurrentTable(api_response,cur):
  cur.execute('''CREATE TABLE IF NOT EXISTS Current(
                  request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  observation_time TEXT, temperature REAL, 
                  weather_code INTEGER,weather_icons TEXT,weather_descriptions TEXT,wind_speed INTEGER,wind_degree INTEGER,wind_dir TEXT, 
                  pressure INTEGER,precip INTEGER,humidity INTEGER,cloudcover INTEGER,feelslike REAL,uv_index INTEGER,
                  visibility INTEGER,is_day TEXT)''')
  
  current_data = api_response["current"]
  flatt(current_data,'weather_icons')
  flatt(current_data,'weather_descriptions')
  insertIntoTable(current_data,'Current',cur)

#This function creates our 3 tables in the local database
def createDB(api_response,cur): 
  createReqTable(api_response,cur)
  createLocationTable(api_response,cur)
  createCurrentTable(api_response,cur)
  return cur

#this function is here to show the connections between our tables,they are connected by the request_id values
def queryTable(cur,tableA,tableB,tableC):
  print('------------------------------------queryTable-----------------------------------------')  
  tableAid = tableA+'.request_id'
  tableBid = tableB+'.request_id'
  tableCid = tableC+'.request_id'
  for row in cur.execute('''SELECT * FROM {}
                              INNER JOIN {} ON {} = {} 
                              INNER JOIN {} ON {} = {} 
                              '''.format(tableA,tableB,tableAid,tableBid,tableC,tableBid,tableCid)):
    print(row)  
  print('------------------------------------queryTable-----------------------------------------\n')  

#function that prints all the rows in a table
def printAllInTable(cur,tableName):
  print('------------------------------------------'+tableName+'-----------------------------------------')
  for row in cur.execute('SELECT * FROM '+tableName):
    print(row)
  print('------------------------------------------'+tableName+'-----------------------------------------\n')

#this function deletes from the database all of the specified tables (if they were already exist)     
def dropAllTables(cur):
  cur.execute('DROP TABLE IF EXISTS Requests')
  cur.execute('DROP TABLE IF EXISTS Locations')
  cur.execute('DROP TABLE IF EXISTS Current') 

def getRequestAndCreateDB(city,unit,cur):    
  res = getRequestToWheaterApi(city,unit)
  api_response = loadWeatherDatatoSqlite3(res)
  createDB(api_response,cur) 

  
def printTables(cur):
  printAllInTable(cur,'Requests')
  printAllInTable(cur,'Locations')
  printAllInTable(cur,'Current')