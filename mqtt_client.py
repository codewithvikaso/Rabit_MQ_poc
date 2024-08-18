# mqtt_client.py
import paho.mqtt.client as mqtt
import pika
import json
import random
import time

# MQTT settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "status_topic"

# RabbitMQ settings
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'mqtt_queue'

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    # Setup RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    # Publish the MQTT message to RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key=RABBITMQ_QUEUE,
                          body=msg.payload)
    print(f"Sent message to RabbitMQ: {msg.payload.decode()}")
    connection.close()

def publish_random_status(client):
    while True:
        status = random.randint(0, 6)
        message = json.dumps({"status": status, "timestamp": time.time()})
        client.publish(MQTT_TOPIC, message)
        print(f"Published message: {message}")
        time.sleep(1)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Start a loop that keeps the connection alive
    client.loop_start()

    # Start publishing random status messages
    publish_random_status(client)
