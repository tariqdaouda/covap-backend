from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Covap!'

@app.route('/api/get_fields', methods=['GET'])
def get_fields():
    return jsonify({'tasks': tasks})

@app.route('/api/get_data', methods=['GET'])
def get_fields():
    return jsonify({'tasks': tasks})