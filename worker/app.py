import pika
import json


def callback(ch, method, properties, body):
    print(json.loads(body))

def main():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue='photo_queue')
    channel.basic_consume(queue='photo_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        print("Now we could connect to the RabbitMQ service.")
        main()
    except:
        raise ValueError("Failed to connect to RabbitMQ service.")