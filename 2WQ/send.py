import pika

import sys

message = ' '.join(sys.argv[1:]) or "Hello World!"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='test2', durable=True)

channel.basic_publish(exchange='',
                      routing_key='test2',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))
print(" [x] Sent 'Hello World!'")
connection.close()