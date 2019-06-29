from django.shortcuts import render

import requests 
import json

# Create your views here.

def write_json(data, filename='answer.json'):
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def process_update(token_bot=None, command = None):
	URL='https://api.telegram.org/bot'
	url = URL+token_bot+'/'+command
	r = requests.get(url)
	write_json(r.json())

