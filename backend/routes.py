from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

# Veriyi yükle
with open(json_url) as f:
    data: list = json.load(f)


######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return jsonify({"message": "Internal server error"}), 500

######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    """Add a new picture"""
    new_picture = request.get_json()

    if not new_picture or "id" not in new_picture:
        return jsonify({"Message": "Invalid input"}), 422  # "Message" anahtarını düzelttik

    # Eğer ID zaten varsa 302 dönmeliyiz
    for picture in data:
        if picture["id"] == new_picture["id"]:
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302  # "Message" anahtarını düzelttik

    data.append(new_picture)
    return jsonify(new_picture), 201  # Yeni resmi tamamen döndürmeliyiz.



######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    updated_data = request.get_json()
    if "id" not in updated_data or updated_data["id"] != id:
        return jsonify({"message": "ID mismatch or missing 'id'"}), 400

    for picture in data:
        if picture["id"] == id:
            picture.update(updated_data)
            return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture"""
    global data
    original_length = len(data)
    data = [pic for pic in data if pic["id"] != id]

    if len(data) < original_length:
        return "", 204  # 204 No Content döndürüyoruz
    return jsonify({"message": "Picture not found"}), 404
