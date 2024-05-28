from flask import Flask, request, jsonify
import requests
import json
import jwt
import time

app = Flask(__name__)

API_SID_KEY = "SK.0.8L1JBosswpzsQGNZujYYwUzpwCncvHSV"
API_SECRET_KEY = "NnFtaGZYZFd2MTQ5bDA2SXdrT0hVVHBrc1JtZFBQSQ=="

# Stringee credentials
API_KEY_SID = API_SID_KEY
API_KEY_SECRET = API_SECRET_KEY

# Generate JWT token
# def generate_jwt():
#     payload = {
#         'jti': API_KEY_SID,
#         'iss': API_KEY_SID,
#         'exp': int(time.time()) + 3600,
#         'userId': 
#     }
#     token = jwt.encode(payload, API_KEY_SECRET, algorithm='HS256')
#     return token

@app.route('/make_call', methods=['POST'])
def make_call():
    data = request.json
    from_number = "+84949521462"
    to_number = "+84905855829"

    url = "https://api.stringee.com/v1/call2"
    headers = {
        'Content-Type': 'application/json',
        'X-STRINGEE-AUTH': 'eyJjdHkiOiJzdHJpbmdlZS1hcGk7dj0xIiwidHlwIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiJTSy4wLjhMMUpCb3Nzd3B6c1FHTlp1allZd1V6cHdDbmN2SFNWLTE3MTY4NzcyNTMiLCJpc3MiOiJTSy4wLjhMMUpCb3Nzd3B6c1FHTlp1allZd1V6cHdDbmN2SFNWIiwiZXhwIjoxNzE5NDY5MjUzLCJ1c2VySWQiOiJkZW1vX3VzZXIifQ.eDsnNDLSV1PiwNnuFTElJcMLZhLPkHjwiJ6ZktuhPjo'
    }
    payload = {
        'from': {
            'type': 'external',
            'number': from_number
        },
        'to': {
            'type': 'external',
            'number': to_number
        },
        'answer_url': 'https://developer.stringee.com/scco_helper/simple_project_answer_url?record=false&appToPhone=auto&recordFormat=mp3'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
