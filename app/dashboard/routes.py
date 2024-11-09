from flask import Blueprint,request, jsonify, current_app
from app.dashboard.models import HumidityLog, PumpActionLog
from app import db , mqtt_client
from datetime import datetime
import paho.mqtt.client as mqtt


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/humidity', methods=['GET'])
def get_humidity():
    humidity_logs = HumidityLog.query.order_by(HumidityLog.timestamp.desc()).limit(10).all()
    result = [
        {
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "humidity_level": log.humidity_level
        } for log in humidity_logs
    ]
    return jsonify(result), 200

@dashboard_bp.route('/pump/status', methods=['GET'])
def get_pump_status():
    last_action = PumpActionLog.query.order_by(PumpActionLog.timestamp.desc()).first()
    if last_action:
        return jsonify({"status": last_action.action}), 200
    return jsonify({"status": "UNKNOWN"}), 200

@dashboard_bp.route('/pump/history', methods=['GET'])
def get_pump_history():
    pump_logs = PumpActionLog.query.order_by(PumpActionLog.timestamp.desc()).limit(10).all()
    result = [
        {
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "action": log.action
        } for log in pump_logs
    ]
    return jsonify(result), 200
@dashboard_bp.route('/pump/control', methods=['POST'])
def control_pump():
    global mqtt_client  
    data = request.get_json()
    command = data.get('command')

    if command not in ["ON", "OFF"]:
        return jsonify({"message": "Invalid command"}), 400

    try:
        if mqtt_client is None:
            broker_address = "broker.hivemq.com"
            mqtt_client = mqtt.Client()  
            mqtt_client.connect(broker_address, 1883, 60)
            mqtt_client.loop_start()

        topic = "actuator/pump"
        mqtt_client.publish(topic, command)
        print(f'Commande "{command}" publiée sur le topic "{topic}"')

        with current_app.app_context():
            pump_action_log = PumpActionLog(action=command, timestamp=datetime.now())
            db.session.add(pump_action_log)
            db.session.commit()
            print(f"Action de la pompe enregistrée: {command}")

        return jsonify({"message": f"Pump turned {command}"}), 200
    except Exception as e:
        print(f"Erreur lors de la publication sur MQTT: {e}")
        return jsonify({"message": "Failed to control pump"}), 500

    data = request.get_json()
    command = data.get('command')
    # Logique pour contrôler la pompe (par exemple via MQTT)
    if command == "ON":
        # Code pour allumer la pompe
        return jsonify({"message": "Pump turned ON"}), 200
    elif command == "OFF":
        # Code pour éteindre la pompe
        return jsonify({"message": "Pump turned OFF"}), 200
    else:
        return jsonify({"message": "Invalid command"}), 400