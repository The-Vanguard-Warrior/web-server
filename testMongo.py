from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://23560092:an23560092@cluster0.drcn4as.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

mongo = MongoClient(app.config['MONGO_URI'])
# mongo = MongoClient('localhost', 27017)
db = mongo.get_database("guardian_database")
collection = db.get_collection("cameras")

@app.route('/')
def index():
    return 'Hello, MongoDB with Flask!'

@app.route('/cameras')
def get_cameras():
    cameras = collection.find({})
    cameras_list = [camera for camera in cameras]
    print(cameras_list)
    return "Successfully fetch users"
    # return render_template('users.html', users=users)

# @app.route('/add_user', methods=['POST'])
# def add_user():
#     name = request.form['name']
#     email = request.form['email']
#     db.users.insert_one({'name': name, 'email': email})
#     return 'User added successfully!'


app.run(debug=True)