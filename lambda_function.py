import os
import json

import emaildispatcher
import requests
import create_video


def lambda_handler(event, context):

	# Generate request to gain a new access key for youtube API
	params = {
		'client_id': os.environ['google_client_id'],
		'client_secret': os.environ['google_client_secret'],
		'refresh_token': os.environ['google_refresh_token'],
		'grant_type': 'refresh_token',
	}

	r = requests.post('https://accounts.google.com/o/oauth2/token', params=params)

	access_token = r.json()['access_token']

	# Generate links using new access token
	amlink = f'https://youtu.be/{create_video.create10AMservice(access_token)}'
	pmlink = f'https://youtu.be/{create_video.create5PMservice(access_token)}'

	# Email the generated links to admin team
	emaildispatcher.sendemail(json.loads(os.environ["email_recipient_list"]), os.environ["email_sender"], [amlink, pmlink])

	return 0
