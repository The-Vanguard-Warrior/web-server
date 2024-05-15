import firebase_admin
from firebase_admin import credentials, messaging
import os
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# This registration token is obtained from the client app when it registers with FCM.
registration_token = os.getenv("REGISTRATION_TOKEN")

def send_notify():
    message = messaging.Message(
        notification=messaging.Notification(
            title='WARNING!!!',
            body='fire fire fire',
        ),
        token=registration_token,
    )

    messaging.send(message)
    print("Successfully"); 

# send_notify()
