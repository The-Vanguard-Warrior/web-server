import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# This registration token is obtained from the client app when it registers with FCM.
registration_token = 'dYpk9ux1SBqi50hF0n-R84:APA91bHh8qioJ-hOfv9QrOKzIyaa5B9Cd9JPKr2VrfPCCsV5VbChQoqC3HMuyL7xrSO6Nl51BufYSWPi6CIpPJ4X2j0LqYWIaVWNx_M1pcOUEE2yl3P9hGKbsoMFFIdgXrMPL9ZN6Ypl'

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
