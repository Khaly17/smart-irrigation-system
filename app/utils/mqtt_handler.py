from app import mqtt, db
from app.dashboard.models import HumidityLog, PumpActionLog
from flask import current_app

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
        mqtt.subscribe("sensor/humidity")
        mqtt.subscribe("actuator/pump")
        print("Subscribed to topics: sensor/humidity, actuator/pump")
    else:
        print(f"Failed to connect to MQTT Broker, return code {rc}")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f'Received message on topic "{topic}": {payload}')

    try:
        with current_app._get_current_object().app_context():
            if topic == "sensor/humidity":
                humidity_level = float(payload)
                humidity_log = HumidityLog(humidity_level=humidity_level)
                db.session.add(humidity_log)
                db.session.commit()
                print(f"Données d'humidité enregistrées: {humidity_level}")

            elif topic == "actuator/pump":
                pump_action_log = PumpActionLog(action=payload)
                db.session.add(pump_action_log)
                db.session.commit()
                print(f"Action de la pompe enregistrée: {payload}")

    except Exception as e:
        print(f"Erreur lors du traitement du message MQTT: {e}")
