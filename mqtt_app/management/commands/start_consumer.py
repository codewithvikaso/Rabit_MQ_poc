import pika
import json
from django.core.management.base import BaseCommand
from mqtt_app.models import StatusMessage
from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'mqtt_db'
MONGO_COLLECTION = 'status_data'

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

class Command(BaseCommand):
    help = 'Starts RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        RABBITMQ_HOST = 'localhost'
        RABBITMQ_QUEUE = 'mqtt_queue'

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        def callback(ch, method, properties, body):
            message = json.loads(body)
            collection.insert_one(message)
            # StatusMessage.objects.create(status=message['status'], timestamp=message['timestamp'])
            print(f"Saved message: {message}")

        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
        print('Waiting for messages...')
        channel.start_consuming()
