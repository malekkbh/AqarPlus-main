from flask import Blueprint, request, jsonify

from website.models import Property, PropertyImage
from website.models import db
from website.dataReq import ADMIN_PASSWORD
from website.send_email import send_email_notification

from website.spaces import (
    upload_file_to_spaces,
    get_spaces_file_cdn_url,
    extract_file_path_from_url,
    delete_file_from_spaces,
)

main_bp = Blueprint("main", __name__)


# Create a new property
@main_bp.route("/properties", methods=["POST"])
def create_property():
    data = request.form.to_dict()

    new_property = Property(
        category=data["category"],
        type=data["type"],
        area=data["area"],
        unit=data["unit"],
        price=data["price"],
        price_for=data["priceFor"],
        currency=data["currency"],
        city=data["city"],
        region=data["region"],
        area_classification=data.get("area_classification"),
        address=data["address"],
        more=data.get("more", ""),
        email=data["email"],
        full_name=data["full_name"],
        phone=data["phone"],
        whatsapp=data["whatsapp"],
        seller_city=data["Seller_city"],
    )

    db.session.add(new_property)
    db.session.commit()

    for file in request.files.getlist("images"):
        if file.filename == "":
            return jsonify("No selected file"), 400

        if file:

            file_path = upload_file_to_spaces(file)

            image_url = get_spaces_file_cdn_url(file_path)

            new_image = PropertyImage(property_id=new_property.id, img=image_url)
            db.session.add(new_image)

    db.session.commit()

    send_email_notification(new_property.id)

    return jsonify({"message": "Property created successfully"}), 201


@main_bp.route("/properties/<int:id>/<string:password>", methods=["PUT"])
def update_property(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401

    property = Property.query.filter_by(id=id).first()
    if not property:
        return jsonify({"error": "Property not found"}), 404

    data = request.form.to_dict()

    new_property = Property(
        category=data["category"],
        type=data["type"],
        area=data["area"],
        unit=data["unit"],
        price=data["price"],
        price_for=data["priceFor"],
        currency=data["currency"],
        city=data["city"],
        region=data["region"],
        area_classification=data.get("area_classification"),
        address=data["address"],
        more=data.get("more", ""),
        email=data["email"],
        full_name=data["full_name"],
        phone=data["phone"],
        whatsapp=data["whatsapp"],
        seller_city=data["Seller_city"],
    )

    # copy the new property data to the existing property
    property.category = new_property.category
    property.type = new_property.type
    property.area = new_property.area
    property.unit = new_property.unit
    property.price = new_property.price
    property.price_for = new_property.price_for
    property.currency = new_property.currency
    property.city = new_property.city
    property.region = new_property.region
    property.area_classification = new_property.area_classification
    property.address = new_property.address
    property.more = new_property.more
    property.email = new_property.email
    property.full_name = new_property.full_name
    property.phone = new_property.phone
    property.whatsapp = new_property.whatsapp
    property.seller_city = new_property.seller_city

    # # get all images for the property and delete them
    # property_images:list[PropertyImage] = PropertyImage.query.filter_by(property_id=property.id).all()

    for file in request.files.getlist("images"):
        if file.filename == "":
            return jsonify("No selected file"), 400

        if file:
            file_path = upload_file_to_spaces(file)

            image_url = get_spaces_file_cdn_url(file_path)

            new_image = PropertyImage(property_id=id, img=image_url)
            db.session.add(new_image)

    db.session.commit()

    return jsonify({"message": "Property updated successfully"}), 200


# Remove Image from the database
@main_bp.route("/remove_image/<int:id>/<string:password>", methods=["POST"])
def remove_image(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401

    image: PropertyImage = PropertyImage.query.get_or_404(id)

    # if image is not found
    if not image:
        return jsonify({"error": "Image not found"}), 404

    file_name = extract_file_path_from_url(image.img)

    delete_file_from_spaces(file_name)

    # === Delete the image from the database ===
    db.session.delete(image)
    db.session.commit()

    return jsonify({"message": "Image deleted successfully from the database"}), 200


# Read all properties
@main_bp.route("/properties/<string:password>", methods=["GET"])
def get_properties(password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401
    properties = Property.query.all()
    properties = [property.to_json() for property in properties]
    return jsonify(properties), 200


# Read a single property by ID
@main_bp.route("/properties/<int:id>/<string:password>", methods=["GET"])
def get_property(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401

    property = Property.query.get_or_404(id)
    property_data = property.to_json()
    return jsonify(property_data), 200


# admin : Publish a property
@main_bp.route("/publish_property/<int:id>/<string:password>", methods=["POST"])
def publish_property(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401
    property: Property = Property.query.get_or_404(id)
    if property.publish_status != "published":
        property.publish_status = "published"
        db.session.commit()
        return jsonify({"message": "Property published successfully"}), 200
    else:
        return jsonify({"message": "Property already published"}), 200


# admin : Unpublish a property
@main_bp.route("/unpublish_property/<int:id>/<string:password>", methods=["POST"])
def unpublish_property(id, password):
    print(password)
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401

    property: Property = Property.query.get_or_404(id)
    if property.publish_status != "unpublished":
        property.publish_status = "unpublished"
        db.session.commit()
        return jsonify({"message": "Property published successfully"}), 200
    else:
        return jsonify({"message": "Property already unpublished"}), 200


# flag a property as sold
@main_bp.route("/sold_property/<int:id>/<string:password>", methods=["POST"])
def sold_property(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401

    property: Property = Property.query.get_or_404(id)
    if property.publish_status != "sold":
        property.publish_status = "sold"
        db.session.commit()
        return jsonify({"message": "Property sold successfully"}), 200
    else:
        return jsonify({"message": "Property already sold"}), 200


# flag a property as rented
@main_bp.route("/rented_property/<int:id>/<string:password>", methods=["POST"])
def rented_property(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401
    property: Property = Property.query.get_or_404(id)
    if property.publish_status != "rented":
        property.publish_status = "rented"
        db.session.commit()
        return jsonify({"message": "Property rented successfully"}), 200
    else:
        return jsonify({"message": "Property already rented"}), 200


# get all published properties
@main_bp.route("/published_properties", methods=["GET"])
def get_published_properties():
    properties = Property.query.filter_by(publish_status="published").all()
    properties = [property.to_json() for property in properties]
    return jsonify(properties), 200


# Delete a property
@main_bp.route("/properties/<int:id>/<string:password>", methods=["DELETE"])
def delete_property(id, password):
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password provided"}), 401

    property = Property.query.get_or_404(id)
    # get all images for the property and delete them
    PropertyImage.query.filter_by(property_id=property.id).delete()

    db.session.delete(property)
    db.session.commit()

    return jsonify({"message": "Property deleted successfully"}), 200


@main_bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({"message": "Server is up and running"}), 200
