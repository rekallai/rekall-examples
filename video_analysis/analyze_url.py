
import requests
import json
import time

REKALL_API_KEY = 'd37011ad9010e67ed4cf8b2ec71952db'
REKALL_AGENT_ID = '592e270165e46500297a15a2'

video_name = 'Teapot Test'
video_url = 'https://storage.googleapis.com/rekall-examples/videos/teapot.mp4'

def create_video(name, video_url):
    req = requests.post('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/videos', **{
        'json': {
            'api_key': REKALL_API_KEY,
            'video_url': video_url,
            'name': name
        }
    })
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

def classify_video(video):
    req = requests.post('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/videos/' + video['_id'] + '/classify', **{
        'json': {
            'api_key': REKALL_API_KEY
        }
    })
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

def get_video_by_id(video_id):
    req = requests.get('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/videos/' + video_id + '?api_key=' + REKALL_API_KEY)
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

def get_video_by_name(name):
    req = requests.get('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/videos?api_key=' + REKALL_API_KEY)
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    for video in res['result']:
        if video['name'] == name:
            return video
    return None

def get_video_analysis(video_id):
    req = requests.get('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/videos/' + video_id + '/analysis?api_key=' + REKALL_API_KEY)
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

def get_video_summary(video_id):
    req = requests.get('http://api.rekall.ai/1/agents/' + REKALL_AGENT_ID + '/videos/' + video_id + '/summary?api_key=' + REKALL_API_KEY)
    res = json.loads(req.text)
    if res.has_key('error'):
        raise Exception('API Error: {}'.format(res['error']['message']))
    return res.get('result', None)

video = get_video_by_name(video_name)
if not video:
    video = create_video(video_name, video_url)
    classify_video(video)
while not video.has_key('status') or video['status']['state'] != 'ready':
    print('Waiting for analysis to complete')
    video = get_video_by_id(video['_id'])
    time.sleep(2)
analysis = get_video_analysis(video['_id'])
summary = get_video_summary(video['_id'])

print('Number of frames analyzed: {}'.format(len(analysis['frames'])))
print('Summary:')
for item in summary['items']:
    if item['labels'][0]['score'] >= 0.60:
        print('{}s: {}'.format(int(item['from_ts']), item['text']))
