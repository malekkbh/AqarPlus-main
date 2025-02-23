from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from website.models import Notification,Property
from website.models import db
from website.dataReq import ADMIN_PASSWORD

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/notifications/<string:password>', methods=['POST'])
def create_notification(password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password"}), 401
    
    data = request.get_json()
    property_id = data.get('property_id')
    title = data.get('title')
    message = data.get('message')

    if not property_id or not title or not message:
        return jsonify({"error": "Missing required fields"}), 400

    new_notification = Notification(
        property_id=property_id,
        title=title,
        message=message
    )
    db.session.add(new_notification)
    db.session.commit()

    return jsonify(new_notification.to_json()), 201


@notification_bp.route('/notifications/<string:password>', methods=['GET'])
def get_notifications(password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    notifications = Notification.query.all()
    return jsonify([notification.to_json() for notification in notifications]), 200

@notification_bp.route('/notifications/<int:id>/<string:password>', methods=['GET'])
def get_notification(id,password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    
    notification = Notification.query.get(id)
    if notification is None:
        return jsonify({"error": "Notification not found"}), 404

    return jsonify(notification.to_json()), 200


@notification_bp.route('/notifications/<int:id>/<string:password>', methods=['PUT'])
def update_notification(id,password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    
    data = request.get_json()
    notification = Notification.query.get(id)
    
    if notification is None:
        return jsonify({"error": "Notification not found"}), 404

    notification.property_id = data.get('property_id', notification.property_id)
    notification.title = data.get('title', notification.title)
    notification.message = data.get('message', notification.message)
    notification.is_read = data.get('is_read', notification.is_read)

    db.session.commit()

    return jsonify(notification.to_json()), 200

@notification_bp.route('/notifications/<int:id>/<string:password>', methods=['DELETE'])
def delete_notification(id,password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}
        ), 401
    notification = Notification.query.get(id)
    
    if notification is None:
        return jsonify({"error": "Notification not found"}), 404

    db.session.delete(notification)
    db.session.commit()

    return jsonify({"message": "Notification deleted"}), 200
