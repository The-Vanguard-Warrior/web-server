from flask import Flask, render_template, Response, jsonify, request, session

# FlaskForm --> It is required to receive input from the user
# Whether uploading a video file to our object detection model

from flask_wtf import FlaskForm

from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os

import cv2

from yolo_functions import video_detection

from pymongo import MongoClient

from fall_function import fall_detection

from twilio_functions import callFireFighter

app = Flask(__name__)
app.config["SECRET_KEY"] = "jackienguyen"
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config["MONGO_URI"] = "mongodb+srv://23560092:an23560092@cluster0.drcn4as.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongo = MongoClient(app.config['MONGO_URI'])
# mongo = MongoClient('localhost', 27017)
db = mongo.get_database("guardian_database")
collection = db.get_collection("cameras")
areas = db.get_collection("areas")

# Use FlaskForm to get input video file and confidence value from user
class UploadFileForm(FlaskForm):
    # We store the uploaded video file and path in the FileField in the variable file
    # We have added validators to make sure the user inputs the video in the valid format and does upload the video when prompted to do so
    file = FileField("File", validators=[InputRequired()])
    # Slider to get confidence value from user
    # conf_slide = IntegerRangeField('Confidence: ', default=25, validators=[InputRequired()])
    submit = SubmitField("Run")

def generate_frames(path_x = ''):
    yolo_output = video_detection(path_x)
    for _, detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# For Webcam
def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    # yolo_output = fall_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     session.clear()
#     return render_template("indexproject.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    cameras = collection.find({})
    camera_list = [camera for camera in cameras]
    return render_template("home_page.html", cameras=camera_list)

@app.route("/call", methods=["POST"])
def call():
    area = request.headers.get('area')
    room = request.headers.get('room')
    # print(area, room)
    # print("received")
    callFireFighter(area, room)
    return jsonify({"message": "Function call() executed successfully"})

# @app.route('/webcam', methods=['GET', 'POST'])
# def webcam():
#     session.clear()
#     return render_template("ui.html")

@app.route('/webcam/<ip>&<id>&<area>&<room>', methods=['GET', 'POST'])
def webcam(ip, id, area, room):
    session.clear()
    result = "Fire"
    # yolo_output = video_detection(path_x=f'http://{ip}:8080/video')
    # for _, class_name in yolo_output:
    #     result = class_name
    return render_template("cam.html", ip=ip, id=id, area=area, room=room)

@app.route('/weblap/<id>&<area>&<room>', methods=['GET', 'POST'])
def webLapCam(id, area, room):
    session.clear()
    result = "Fire"
    # yolo_output = video_detection(path_x=f'http://{ip}:8080/video')
    # for _, class_name in yolo_output:
    #     result = class_name
    return render_template("uic.html", id=id, area = area, room=room)

@app.route('/FrontPage', methods=['GET', 'POST'])
def front():
    form = UploadFileForm()
    if form.validate_on_submit():
        # Our uploaded video file path is saved heref
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], 
                               secure_filename(file.filename))) # Then save the file 
        # Use session storage to save video file path and confidence value 
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], 
                                             secure_filename(file.filename))
        
    return render_template('videoprojectnew.html', form=form)

@app.route('/video')
def video():
    return Response(generate_frames(path_x=session.get('video_path', None)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/add_camera')
def add_camera():
    area_list = areas.find({})
    area_options = [area for area in area_list]
    print(area_options)
    room_options = []
    for area_option in area_options:
        for room in area_option['room_list']:
            room_options.append(room)
    return render_template("add_camera.html", area_options=area_options, room_options=room_options)

@app.route('/add_location')
def add_location():
    return render_template("add_location.html")

@app.route('/web')
def web():
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webapp/<ip>')
def webapp(ip):
    return Response(generate_frames_web(path_x=f'http://{ip}:8080/video'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/post_camera', methods=["POST"])
def post_camera():
    ip_address = request.form['ip_address']
    device_type = request.form['device_type']
    area = request.form['area']
    room = request.form['room']

    # Save the data to MongoDB
    camera_data = {
        'ip_address': ip_address,
        'ipCam': True if device_type == "ip_cam" else False,
        'area': area,
        'room': room
    }
    camera_added = collection.insert_one(camera_data)
    camera_id = str(camera_added.inserted_id)
    collection.update_one({'_id': camera_added.inserted_id}, {"$set": {'id': camera_id}})

    return 'Camera data uploaded successfully'

@app.route('/post_area', methods=["POST"])
def post_area():
    area = request.form['area']
    rooms = request.form['room_list']
    room_list = rooms.split(",")

    area_data = {
        'area': area,
        'room_list': room_list
    }
    area_added = areas.insert_one(area_data)
    area_id = str(area_added.inserted_id)
    areas.update_one({'_id': area_added.inserted_id}, {"$set": {"area_id": area_id}})
    # print(f'{area}: {room_list}')

    return "Area added successfully"


@app.route('/delete_cam', methods=['DELETE'])
def delete_cam():
    # Delete the camera data from MongoDB
    camera_id = request.headers.get('Camera-ID')

    # Delete the camera data from MongoDB
    result = collection.delete_one({'id': camera_id})

    if result.deleted_count > 0:
        return 'Camera deleted successfully'
    else:
        return 'Error deleting camera', 404


app.run(debug=True)