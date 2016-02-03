import json
import requests
from django.conf import settings

APP_ID = getattr(settings, 'PUSHWOOSH_APP_ID', '')
AUTH_TOKEN = getattr(settings, 'PUSHWOOSH_AUTH_TOKEN', '')

def _create_message(devices, notification):
    message = {'request':
                {'application': APP_ID,
                    'auth': AUTH_TOKEN,
                    'notifications': [{
                        'send_date': 'now',
                        'content': notification.getTitle(),
                        'data': notification.getExtra(),
                        'devices' : devices}]
                }
            }
    return message

def send_request(devices, notification):
    URL = u'https://cp.pushwoosh.com/json/1.3/createMessage'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(_create_message(devices, notification))
    
    response = requests.post(URL, payload.encode('utf8'), headers=headers)
        
    if response and response.status_code == 200:
        notification.pw_response = response.json()
        notification.sent  = True
        notification.save()
        return response.json()
    else:
        return {}
