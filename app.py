from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB-USERNAME')}:{os.getenv('DB-PASSWORD')}@{os.getenv('DB-HOST')}:{os.getenv('DB-PORT')}/{os.getenv('DB-NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define the Name model
class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Endpoint to add a name
@app.route('/add_name', methods=['POST'])
def add_name():
    data = request.json
    name = data.get('name')
    if name:
        new_name = Name(name=name)
        db.session.add(new_name)
        db.session.commit()
        return jsonify({'message': 'Name added successfully!'}), 200
    return jsonify({'error': 'Name not provided!'}), 400

# Endpoint to get all names
@app.route('/get_names', methods=['GET'])
def get_names():
    all_names = Name.query.all()
    name_list = [{'id': name.id, 'name': name.name} for name in all_names]
    return jsonify({'names': name_list}), 200

# Endpoint for the main page
@app.route('/', methods=['GET'])
def home():
    return 'Hello, 123!'

if __name__ == '__main__':
    app.run(debug=True)
