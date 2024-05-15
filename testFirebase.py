
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app

# Initialize Firebase app
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Route to render cameras page
    # Fetch camera information from Firestore
cameras_ref = db.collection('cameras')
cameras = cameras_ref.get()
camera_data = [camera.to_dict() for camera in cameras]

print(camera_data)

