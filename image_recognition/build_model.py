
import os
import requests
import json
import time

REKALL_API_KEY = 'd37011ad9010e67ed4cf8b2ec71952db'

model_name = 'Indoor VS Outdoor'
classes = {
    'Indoor': 'files/indoor_vs_outdoor/indoor',
    'Outdoor': 'files/indoor_vs_outdoor/outdoor'
}

def call_api(method, path, params):
    options = {}
    if method == 'GET':
        options['params'] = params
    else:
        options['json'] = params
    options['headers'] = {'X-Api-Key': REKALL_API_KEY}
    req = requests.request(method, 'https://api.rekall.ai/1' + path, **options)
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

# Upload file, and get back an image object
def upload_class_image(model, klass, path):
    req = requests.post('https://api.rekall.ai/1/models/{}/classes/{}/upload'.format(model['_id'], klass['_id']), **{
        'files': {
            'file': open(path,'rb')
        },
        'headers': {
            'X-Api-Key': REKALL_API_KEY
        }
    })
    res = json.loads(req.text)
    if res.has_key('error'):
        if 'already added' in res['error']['message']:
            return None
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res['result']

def get_model_by_name(model_name):
    models = call_api('GET', '/models', {'mine': True})
    for model in models:
        if model['name'] == model_name:
            return model
    return None

def get_class_by_name(model, class_name):
    classes = call_api('GET', '/models/{}/classes'.format(model['_id']), {})
    for klass in classes:
        if klass['name'] == class_name:
            return klass
    return None

def generate_slug(str):
    return str.lower().replace(' ', '-')

# Create a new model if it doesn't exist yet
model = get_model_by_name(model_name)
if not model:
    print('Creating new model')
    model = call_api('POST', '/models', {
        'name': model_name,
        'type': 'image_classification',
        'slug': generate_slug(model_name)
    })
model_id = model['_id']

# For each image directory, create a class and upload images
for class_name in classes:
    klass = get_class_by_name(model, class_name)
    if not klass:
        print('Adding class: {}'.format(class_name))
        klass = call_api('POST', '/models/{}/classes'.format(model_id), {'name': class_name})
    image_dir = classes[class_name]
    image_files = [f for f in os.listdir(image_dir)]
    images = call_api('GET', '/models/{}/classes/{}/images'.format(model_id, klass['_id']), {})
    if len(images) == len(image_files):
        continue
    for file_path in image_files:
        full_path = image_dir + '/' + file_path
        if os.path.isfile(full_path):
            print('Uploading file: {}'.format(full_path))
            upload_class_image(model, klass, full_path)

# Start build process
if not model.has_key('status'):
    print('Building model instance')
    call_api('POST', '/models/{}/build'.format(model_id), {})

# Wait for model to be built
while not model.has_key('status') or model['status']['state'] != 'ready':
    status = model.get('status', None)
    if status:
        print('Status: {} ({}/{})'.format(status['state'], status.get('current', 0), status.get('total', 1)))
    else:
        print('Model build initializing')
    time.sleep(2)
    model = call_api('GET', '/models/{}'.format(model_id), {})
print('Model {} successfully built, create an Agent to deploy'.format(model_id))
