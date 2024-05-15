from twilio.rest import Client

def callFireFighter(area, room):
    account_sid = 'AC63d6b4da907533c627b381a7bd48cee5'
    auth_token = '6197bafdc9d45f67b78e015bb272b77d'
    client = Client(account_sid, auth_token)

    client.calls.create(
        twiml=f'<Response><Say>Warning, there is a fire incident in area {area}, room {room}.</Say></Response>',
        to='+84949521462',
        from_='+12676338251'
    )
