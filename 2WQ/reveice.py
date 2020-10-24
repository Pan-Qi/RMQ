#!/usr/bin/env python
import pika

import time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='test2', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag) # 处理完通知queue

    channel.basic_qos(prefetch_count=1) # 选择空闲的consumer，分发一个message

    channel.basic_consume(queue='test2', on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')