from WeatherDB import dropAllTables,getRequestAndCreateDB,printTables,cur,queryTable

def main(): 
  #delete the tables if they are already exists  
  dropAllTables(cur)
  
  #for each request to the weather api we need to call getRequestAndCreateDB with that city name and the unit and with the connection to the data base
  getRequestAndCreateDB('Tel Aviv','f',cur) 
  getRequestAndCreateDB('New York','f',cur) 
  getRequestAndCreateDB('Madrid','f',cur) 
  
  #print all the tables we created
  printTables(cur)

  queryTable(cur,'Requests','Locations','Current')   
  
  #close the local db connection
  cur.close()

if __name__ == "__main__":
    main()
