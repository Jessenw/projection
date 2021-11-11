# Projection

## Setup

### RabbitMQ

To start the RabbitMQ server, run:
`sudo rabbitmq-server`

### Celery

To start the Celery worker, run:
`celery -A <parent-folder> worker -l INFO`