from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pika

app = FastAPI()

origins = ["*"]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройки для RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='button_sequence')
except pika.exceptions.AMQPConnectionError as e:
    print(f"Error connecting to RabbitMQ: {e}")
    exit(1)


# Функция-обработчик сообщений
def callback(ch, method, properties, body):
    try:
        print(f"Received message: {body}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Подписываемся на очередь и запускаем бесконечный цикл ожидания сообщений
try:
    channel.basic_consume(queue='button_sequence', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
except Exception as e:
    print(f"Error consuming messages from RabbitMQ: {e}")
    exit(1)


# Маршруты FastAPI
@app.post('/button1')
async def save_button1(request: Request):
    try:
        # Сохраняем данные в RabbitMQ
        message = request.json()
        channel.basic_publish(exchange='', routing_key='button_sequence', body=message)
        return {'status': 'success'}
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")
        return {'status': 'error'}


@app.post('/button2')
async def save_button2(request: Request):
    try:
        # Сохраняем данные в RabbitMQ
        message = request.json()
        channel.basic_publish(exchange='', routing_key='button_sequence', body=message)
        return {'status': 'success'}
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")
        return {'status': 'error'}


@app.post('/button3')
async def save_button3(request: Request):
    try:
        # Сохраняем данные в RabbitMQ
        message = request.json()
        channel.basic_publish(exchange='', routing_key='button_sequence', body=message)
        return {'status': 'success'}
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")
        return {'status': 'error'}


# Обработчик для маршрута, принимающего POST-запросы с последовательностью кнопок
@app.post("/api/sequence")
async def receive_sequence(sequence: list):
    if len(sequence) != 3:
        raise HTTPException(status_code=400, detail="Invalid sequence length")

    # Возвращаем ту же последовательность, которую приняли
    return {"sequence": sequence}


# Обработчик для RabbitMQ сообщений
def handle_message(channel, method, properties, body):
    print("Received sequence:", body.decode())


# Слушаем очередь для сообщений
channel.basic_consume(queue='button_sequence', on_message_callback=handle_message, auto_ack=True)


# Запускаем поток для прослушивания очереди
def listen_to_queue():
    channel.start_consuming()