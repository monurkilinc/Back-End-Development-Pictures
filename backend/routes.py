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
    """Find and return picture by id"""
    picture = next((p for p in data if p["id"] == id), None)
    if picture:
        return jsonify(picture), 200  # Başarıyla bulunduysa 200 OK
    return jsonify({"error": "Picture not found"}), 404  # Bulunamadıysa 404

######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry"""
    picture = request.get_json()
    if "id" not in picture:
        return jsonify({"Message": "Invalid data, 'id' field required"}), 400
    if any(p["id"] == picture["id"] for p in data):
        return jsonify({"Message": "picture with id 200 already present"}), 302
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    updated_data = request.get_json()

    for picture in data:
        if picture["id"] == id:
            picture.update(updated_data)
            return jsonify(picture), 200

    return jsonify({"message": "resim bulunamadı"}), 404

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture from the database"""
    global data
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204  # No Content

    return jsonify({"message": "resim bulunamadı"}), 404

