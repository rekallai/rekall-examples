
import requests
import json
import time

REKALL_API_KEY = 'd37011ad9010e67ed4cf8b2ec71952db'
REKALL_AGENT_ID = '58feaa5782b0d80012c637ed'

# Upload file, and get back an image object
def upload_image(path):
    req = requests.post('https://api.rekall.ai/1/cache/image/upload', **{
        'files': {
            'file1': open(path,'rb')
        },
        'data': {
            'api_key': REKALL_API_KEY
        }
    })
    return json.loads(req.text)['result'][0]

# Classify image object, returns None when queued, raises Exception on error
def classify(image):
    req = requests.post('https://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/run', **{
        'json': {
            'api_key': REKALL_API_KEY,
            'image_url': image['image_url'],
            'image_uid': image['image_uid']
        }
    })
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

# Upload image, and wait for result
image = upload_image('files/lake.jpg')
result = None
while not result:
    result = classify(image)
    time.sleep(2)
print(result)
