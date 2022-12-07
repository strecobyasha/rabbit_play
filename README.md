# RabbitMQ Playground

***
This is a simple playground for RabbitMQ. It allows you to send and receive messages through broker 
(aio-pika in this case). It also implements the mechanism of sending the message back to broker and keep it
their for some time (delayed messages). For that purpose you need to create a queue without a consumer.

***
Generator - creates messages.

Worker - receive messages.

Broker - just broker.

***
To start:

1) make build (will launch Rabbit container via Docker).
2) Manually start a script worker.py
3) Manually start a script generator.py
