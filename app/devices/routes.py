from flask import Blueprint, request, jsonify
from app import db, mqtt_client  
from app.devices.models import Device

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    device = Device.query.get_or_404(device_id)
    device.status = 'ON' if device.status == 'OFF' else 'OFF'
    db.session.commit()

    if mqtt_client:
        mqtt_client.publish(f'devices/{device.name}/status', device.status)

    return jsonify({'message': f'Device {device.name} toggled to {device.status}'}), 200

@devices_bp.route('/pump', methods=['POST'])
def control_pump():
    data = request.get_json()
    command = data.get('command')

    if command not in ["ON", "OFF"]:
        return jsonify({'error': 'Invalid command. Use "ON" or "OFF"'}), 400

    if mqtt_client:
        mqtt_client.publish("actuator/pump", command)

    return jsonify({'message': f'Command "{command}" sent to the pump'}), 200

@devices_bp.route('/test_publish', methods=['GET'])
def test_publish():
    if mqtt_client:
        mqtt_client.publish("sensor/humidity", "15")
    return jsonify({'message': 'Test message sent'}), 200
