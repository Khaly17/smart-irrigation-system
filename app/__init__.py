from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import paho.mqtt.client as mqtt
from flask_cors import CORS
import threading
import os
import math
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
mqtt_client = None
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

    from app.auth.routes import auth_bp
    from app.devices.routes import devices_bp
    from app.dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    # if not os.getenv("FLASK_SKIP_MQTT"):
    #     threading.Thread(target=init_mqtt, args=(app,), daemon=True).start()

    return app

# def init_mqtt(app):
#     global mqtt_client
#     if mqtt_client is None:
#         broker_address = "broker.hivemq.com" 
#         mqtt_client = mqtt.Client("FlaskMQTTClient")

#         mqtt_client.connect(broker_address, 1883, 60)

#         mqtt_client.on_connect = lambda client, userdata, flags, rc: on_connect(client, userdata, flags, rc, app)
#         mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, app)

#         mqtt_client.loop_start()
#     else:
#         print("Client MQTT déjà initialisé")

# def on_connect(client, userdata, flags, rc, app):
#     if rc == 0:
#         print("Connected to MQTT Broker successfully!")
#         client.subscribe("sensor/humidity")
#         client.subscribe("actuator/pump")
#         print("Subscribed to topics: sensor/humidity, actuator/pump")
#     else:
#         print("Failed to connect to MQTT Broker, return code {rc}")

# def on_message(client, userdata, message, app):
#     from app.dashboard.models import HumidityLog, PumpActionLog

#     topic = message.topic
#     payload = message.payload.decode()
#     print(f'Received message on topic "{topic}": {payload}')

#     try:
#         with app.app_context():
#             if topic == "sensor/humidity" and payload.lower() != 'nan':
#                 try:
#                     humidity_level = float(payload)

#                     last_log = HumidityLog.query.order_by(HumidityLog.timestamp.desc()).first()

#                     if last_log is None or not math.isclose(float(last_log.humidity_level), float(humidity_level), rel_tol=1e-9):
#                         humidity_log = HumidityLog(humidity_level=humidity_level)
#                         db.session.add(humidity_log)
#                         db.session.commit()
#                         print(f"Données d'humidité enregistrées: {humidity_level}")
#                     else:
#                         print(f"Aucune modification détectée pour l'humidité: {humidity_level}")

#                 except ValueError:
#                     print(f"Erreur de conversion : le payload '{payload}' ne peut pas être converti en float.")

#             elif topic == "actuator/pump":
#                 last_action_log = PumpActionLog.query.order_by(PumpActionLog.timestamp.desc()).first()
#                 if last_action_log is None or last_action_log.action != payload:
#                     pump_action_log = PumpActionLog(action=payload)
#                     db.session.add(pump_action_log)
#                     db.session.commit()
                    
#                     print(f"Action de la pompe enregistrée: {payload}")
#                 else:
#                     print(f"Aucune nouvelle action détectée pour la pompe: {payload}")

#     except Exception as e:
#         print(f"Erreur lors du traitement du message MQTT: {e}")

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
