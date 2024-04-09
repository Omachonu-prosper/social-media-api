from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    return jsonify({
        'message': 'You have hit the index route',
        'status': True,
    }), 200