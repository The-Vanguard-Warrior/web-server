from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def callFireFighter(area, room):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    client.calls.create(
        twiml=f'<Response><Say>Warning, there is a fire incident in area {area}, room {room}.</Say></Response>',
        to=os.getenv("TO_NUMBER"),
        from_=os.getenv("FROM_NUMBER")
    )
