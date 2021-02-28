# WeatherDB

## The project containing the following files:
1. WeatherDB.py 
2. main.py
3. test_sample.py

## WeatherDB.py 

The function getRequestToWheaterApi is sending a get request to weatherstack api.
I choose to save the data in local JSON file named 'Cityname_Weather_Info.json' for each request in JSON_files folder.
After looking at the JSON file i saw that it has 3 main keys which is request, location and current,
so i decided to cerate 3 different tables with sqlite3 databae, and connecting all of the tables by the request_id column,
the request_id is an incremented column.

Each time we send a request to the weahterstack api we increment the request_id and adding to our 3 tables the data.
I've added a print function name printTables which prints all of the tables.

## main.py

Here we send all of the requests to the weather api, it runs the whole flow of the assignment and printing the tables we create.


## test_sample

some tests that running by pytest.
