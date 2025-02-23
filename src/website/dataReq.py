from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from website.models import DataReq, Property
from website.models import db

data_reqs_bp = Blueprint('data_reqs_bp', __name__)
# give me instructions to create a strong random password
# 1. import the secrets module
# 2. use secrets.token_urlsafe() to generate a random password

ADMIN_PASSWORD = 'kljSd931@nVcx'

# Create a new data request
@data_reqs_bp.route('/data_reqs', methods=['POST'])
def create_data_req():
    data = request.json

    # Fetch the associated property
    property = Property.query.get(data.get('property_id'))
    if not property:
        abort(404, description="Property not found")

    new_data_req = DataReq(
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        number_of_individuals=data.get('number_of_individuals'),
        city=data.get('city'),
        is_sale=data.get('is_sale', True),
        property_id=property.id
    )

    db.session.add(new_data_req)
    db.session.commit()

    return jsonify(new_data_req.to_json()), 201

# Read (Retrieve) all data requests
@data_reqs_bp.route('/data_reqs/<string:password>', methods=['GET'])
def get_data_reqs(password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    
    data_reqs = DataReq.query.all()
    return jsonify([data_req.to_json() for data_req in data_reqs])

# Read (Retrieve) a single data request by ID
@data_reqs_bp.route('/data_reqs/<int:id>/<string:password>', methods=['GET'])
def get_data_req(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    data_req = DataReq.query.get_or_404(id)
    return jsonify(data_req.to_json())

# Update an existing data request by ID
@data_reqs_bp.route('/data_reqs/<int:id>/<string:password>', methods=['PUT'])
def update_data_req(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    data = request.json
    data_req = DataReq.query.get_or_404(id)
 
    # Update the fields
    data_req.full_name = data.get('full_name', data_req.full_name)
    data_req.phone = data.get('phone', data_req.phone)
    data_req.number_of_individuals = data.get('number_of_individuals', data_req.number_of_individuals)
    data_req.city = data.get('city', data_req.city)
    data_req.is_sale = data.get('is_sale', data_req.is_sale)
    
    # Update the property if provided
    property_id = data.get('property_id')
    if property_id:
        property = Property.query.get(property_id)
        if not property:
            abort(404, description="Property not found")
        data_req.property_id = property.id

    db.session.commit()

    return jsonify(data_req.to_json())

# Delete a data request by ID
@data_reqs_bp.route('/data_reqs/<int:id>/<string:password>', methods=['DELETE'])
def delete_data_req(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    
    data_req = DataReq.query.get_or_404(id)

    db.session.delete(data_req)
    db.session.commit()

    return jsonify({'message': 'Data request deleted successfully'}), 200
