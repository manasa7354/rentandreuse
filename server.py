from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# -----------------------------
# UPLOAD FOLDER
# -----------------------------

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# CORS
# -----------------------------

@app.after_request
def add_cors_headers(response):

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    return response


# -----------------------------
# HOME / TEST
# -----------------------------

@app.route("/")
def home():

    return "Rent and Reuse backend is running"


# -----------------------------
# IMAGE UPLOAD
# -----------------------------

@app.route("/upload-image", methods=["POST"])
def upload_image():

    if "image" not in request.files:

        return jsonify({
            "error": "No image selected"
        }), 400

    image = request.files["image"]

    if image.filename == "":

        return jsonify({
            "error": "No image selected"
        }), 400

    filename = image.filename

    image.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )

    return jsonify({

        "message": "Image uploaded successfully",

        "imageURL": "/uploads/" + filename

    })


# -----------------------------
# SHOW UPLOADED IMAGE
# -----------------------------

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# -----------------------------
# REQUEST ITEM
# -----------------------------

requests_list = []


@app.route("/requests", methods=["POST", "OPTIONS"])
def create_request():

    # Handle browser preflight request
    if request.method == "OPTIONS":

        return jsonify({
            "message": "CORS OK"
        })


    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No request data received"
        }), 400


    item_id = data.get("item_id")
    requester = data.get("requester")
    requester_email = data.get("requester_email")
    request_type = data.get("type")


    if not item_id:

        return jsonify({
            "error": "Item ID is missing"
        }), 400


    if not requester:

        return jsonify({
            "error": "Requester name is missing"
        }), 400


    if not requester_email:

        return jsonify({
            "error": "Requester email is missing"
        }), 400


    if request_type not in ["Rent", "Borrow"]:

        return jsonify({
            "error": "Invalid request type"
        }), 400


    new_request = {

        "id": len(requests_list) + 1,

        "item_id": item_id,

        "requester": requester,

        "requester_email": requester_email,

        "type": request_type,

        "status": "Pending"
    }


    requests_list.append(new_request)


    print("NEW REQUEST:")
    print(new_request)


    return jsonify({

        "message": "Request sent successfully",

        "request": new_request

    }), 201


# -----------------------------
# GET REQUESTS
# -----------------------------

@app.route("/requests", methods=["GET"])
def get_requests():

    return jsonify(requests_list)


# -----------------------------
# START SERVER
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )