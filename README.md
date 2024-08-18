# MQTT-RabbitMQ-MongoDB Integration Project
## Project Overview
This project demonstrates a client-server architecture where MQTT messages are transmitted via RabbitMQ, processed by a Python server, 
and stored in MongoDB. The server also provides an endpoint to retrieve the count of different statuses within a specified time range.
## Features
- MQTT Messaging via RabbitMQ: A client script emits MQTT messages every second containing a random status value (0-6).
- Message Processing and Storage: The server processes these messages and stores them in MongoDB.
- Data Retrieval Endpoint: The server provides an endpoint to retrieve the count of each status within a specified time range using MongoDB’s aggregation framework.
## Prerequisites
Ensure the following software is installed on your Windows machine:
- Python 3.x
- RabbitMQ
- MongoDB
- https://mosquitto.org/download/ (download and install for windows machine)
## Steps foe Execute the  project
1) create virtual environment
   - python -m venv rabbitmq_env
2) activate environment
   - .\rabbitmq_env\Script\activate
3)install libraries
  - pip install -r requirements.txt
4) open mongodb compass for create mqtt_db database
   - open mongosh terminal and write
   - use mqtt_db;  #this command create the database
5) start django project
  - python manage.py runserver
6) start rabbitMq start_consumer file using new terminal and activate env
   - python manage.py start_consumer
7) open cmd and start mosquitto for mqtt server
  - C:\Users\My Pc>mosquitto
8) start python script in virtual environment using new terminal
  - in my case: (rabit_env) F:\RabitMQ_poc\rabitMQ_Pro>python mqtt_client.py
9)check database table
