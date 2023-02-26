from flask import Flask
from flask_restful import Api, reqparse, Resource
import pika
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('path', type=str)

class ApiUploadPhoto(Resource):
    def post(self):
        args = parser.parse_args()

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to RabbitMQ service. Photo wont be sent.")
            return
        
        channel = connection.channel()
        channel.queue_declare(queue='photo_queue')

        channel.basic_publish(
            exchange='',
            routing_key='photo_queue',
            body=json.dumps(args),
        )

        return {'path' : args['path']}


api.add_resource(ApiUploadPhoto, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)