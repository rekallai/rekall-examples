
import requests
import json
import time

REKALL_API_KEY = 'd37011ad9010e67ed4cf8b2ec71952db'
REKALL_AGENT_ID = '58feaa5782b0d80012c637ed'

image_url = 'https://storage.googleapis.com/rekall-examples/classification/lake.jpg'

# Classify image url, returns None when queued, raises Exception on error
def classify_url(image_url):
    req = requests.post('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/run', **{
        'json': {
            'api_key': REKALL_API_KEY,
            'image_url': image_url
        }
    })
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

result = None
while not result:
    result = classify_url(image_url)
    time.sleep(2)
print(result)
