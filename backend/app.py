
from flask import Flask, jsonify, request
from flask_cors import CORS
from routes import router

app = Flask(__name__)
CORS(app)

app.register_blueprint(router, url_prefix="/api")

@app.route('/')
def hello():
    return "Intelligent Parcel Delivery Backend is running."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
