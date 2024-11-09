import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Richter2.0')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'arrosage_db')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    MQTT_BROKER_URL = 'test.mosquitto.org'  
    MQTT_BROKER_PORT = 1883
    MQTT_USERNAME = '' 
    MQTT_PASSWORD = ''
    MQTT_KEEPALIVE = 60
    MQTT_TLS_ENABLED = False
