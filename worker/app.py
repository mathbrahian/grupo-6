import pika
import json
from sqlalchemy import create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker
import base64

engine = create_engine('sqlite:////tmp/photo.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Photo(Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    path = Column(String)
    binary = Column(LargeBinary)
    def __repr__(self):
        return f"<Photo(id={self.id}, path={self.path})>"

Base.metadata.create_all(engine)

def callback(ch, method, properties, body):
    with open(json.loads(body)["path"], "rb") as img_file:
        photo_binary = base64.b64encode(img_file.read())
    photo = Photo(path=json.loads(body)["path"], binary=photo_binary)
    session.add(photo)
    session.commit()
    print(photo)


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