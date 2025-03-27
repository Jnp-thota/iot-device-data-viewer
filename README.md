# IOT Device Project:
	Terminology:	Different sensor devices are placed in different type of rooms(Office, Living Room, BedRoom,..etc) our Project daily deals with collection all the sensor data from the sensors in the specific time interval and used this data to build a effective UI that help customer to monitor the device performance  and do some CURD operations if any new device added or any information related to device is changed.

# REST API built using API Gateway:
	Device level API’s:
		Adding New Device: End point: /devices, Method: POST, Request Body: Device info in JSON format.
		Get all Devices Data : End Point:/devices, Method : GET
		Get one Device Data: End Point:/devices/{device_id}, Method : GET
		Edit or Update or change Device Information: End Point: /device/{device_id} Method : PUT
		Delete a Device: End Point: /devices/{device_id} Method : DELETE
	Time Series Data:
		Get Time Series of Particular Device: End Point:/timeseries Params : deviceId =1 Method : GET



# DataBase Details :
	Created a MySQL DataBase with two tables for the Project:
		1. Devies
		2. TimeSeries

	DataBase Script for creation and inserting initial details to test:
		CREATE DATABASE initial_db;
    USE initial_db;
    CREATE TABLE devices ( device_id bigint unsigned NOT NULL, building_name varchar(255) NOT NULL, floor int NOT NULL, zone varchar(255) NOT NULL, room_name varchar(255) NOT NULL, user_notes text, room_type varchar(255) NOT NULL, PRIMARY KEY (device_id), UNIQUE KEY device_id (device_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    CREATE TABLE time_series_data ( id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, device_id BIGINT UNSIGNED NOT NULL, timestamp TIMESTAMP NOT NULL, metric_value FLOAT NOT NULL, temperature FLOAT DEFAULT NULL, humidity FLOAT DEFAULT NULL, pressure FLOAT DEFAULT NULL, co2 FLOAT DEFAULT NULL, PRIMARY KEY (id), FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    INSERT INTO devices (device_id, building_name, floor, zone, room_name, user_notes, room_type) VALUES (101, 'Building A', 1, 'Zone 1', 'Room 101', 'Test device', 'Office'); INSERT INTO time_series_data (device_id, timestamp, temperature, humidity, pressure, co2) VALUES (101, '2025-03-25 08:00:00', 22.5, 45.0, 1012.3, 400.5), (101, '2025-03-25 09:00:00', 23.1, 47.2, 1011.8, 410.2), (101, '2025-03-25 10:00:00', 24.0, 50.0, 1010.6, 420.7), (101, '2025-03-25 11:00:00', 25.3, 52.1, 1009.9, 430.0);

	
# Technologies used:
	React JS
	Python
	SQL
	AWS Cloud Technologies :
      Amplify
      API Gateway
      Lambda
      RDS(MySQL)
      Cloud Watch








