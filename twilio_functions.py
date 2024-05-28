from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def callFireFighter(area, room):
    account_sid = "AC5268c8b1697edd45130d3a70871566e9"
    auth_token = "910c6ebdc80e1c09b1f7ead19408529e"
    client = Client(account_sid, auth_token)

    client.calls.create(
        twiml=f'<Response><Say>Warning, there is a fire incident in area {area}, room {room}.</Say></Response>',
        to="+840905855829",
        from_="+13515297825"
    )



callFireFighter(1, 1.2)