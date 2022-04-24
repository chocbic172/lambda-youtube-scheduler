import datetime
import time

import json
import requests

def suffix(d):
	# Adds suffixes to dates (5th, 22nd, etc.)
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')


def nextsunday():
	# Finds date of next sunday as a datetime object. Also returns wether or not daylights savings applies

	daylightsavings = time.localtime().tm_isdst # TODO: Checks CURRENT daylight savings NOT following sunday's DST. Will break 2x per year.
	
	daylightsavings = 1 # hacky fix for BST

	today = datetime.datetime.today()
	sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )

	return sunday, daylightsavings

def addthumbnail(id, image, access_token):
	# API call to add thumbnail to video

	headers = {
		'Authorization': f'Bearer {access_token}',
		'Accept': 'application/json'
	}

	# Uploads file (passed as parameter)
	files = {'file': open(image, 'rb')}
	d = requests.post(f'https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={id}', headers=headers, files=files)

	# Debugging
	if d.status_code != requests.codes.ok:
		print(d.json())


def create10AMservice(access_token):
	# Generates a 10AM service livestream based on following template
	sunday, daylightsavings = nextsunday()

	# Generates tile and start time (accounting for daylight savings)
	title = f'10AM Livestream - {sunday.strftime(f"%#d{suffix(sunday.day)} %B")}'
	scheduled_start = sunday.replace(hour=9-daylightsavings, minute=45, second=0, microsecond=0).isoformat() + 'Z'

	# Set up request
	headers = {
		'Authorization': f'Bearer {access_token}',
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	# Generate livestream from template
	data = {
		"kind": "youtube#liveBroadcast",
		"snippet": {
			"title": title,
			"description": "Join us for our 10AM livestream service. Everyone welcome!",
			"scheduledStartTime": scheduled_start,
		},
		"contentDetails": {
			"enableEmbed": True,
			"enableDvr": True,
			"enableContentEncryption": False,
			"startWithSlate": False,
			"recordFromStart": True,
			"enableClosedCaptions": False,
			"enableLowLatency": False,
			"latencyPreference": "normal",
			"enableAutoStart": False,
			"enableAutoStop": False
		},
		"status": {
			"privacyStatus": "public",
			"selfDeclaredMadeForKids": False,
		}
	}

	# Send API request
	r = requests.post('https://youtube.googleapis.com/youtube/v3/liveBroadcasts?part=snippet%2CcontentDetails%2Cstatus', headers=headers, data=json.dumps(data))

	# Debugging
	print(r.json())
	parsed_response = r.json()
	parsed_id = parsed_response['id']

	# Add thumbnail to generated livestream. Return ID.
	addthumbnail(parsed_id, '10am-thumb.jpg', access_token)

	return parsed_id

def create5PMservice(access_token):
	# Generates a 5PM service livestream based on following template
	sunday, daylightsavings = nextsunday()

	# Generates tile and start time (accounting for daylight savings)
	title = f'5PM Livestream - {sunday.strftime(f"%#d{suffix(sunday.day)} %B")}'
	scheduled_start = sunday.replace(hour=16-daylightsavings, minute=45, second=0, microsecond=0).isoformat() + 'Z'

	# Set up request
	headers = {
		'Authorization': f'Bearer {access_token}',
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	# Generate livestream from template
	data = {
		"kind": "youtube#liveBroadcast",
		"snippet": {
			"title": title,
			"description": "Join us for our 5PM livestream service. Everyone welcome!",
			"scheduledStartTime": scheduled_start,
		},
		"contentDetails": {
			"enableEmbed": True,
			"enableDvr": True,
			"enableContentEncryption": False,
			"startWithSlate": False,
			"recordFromStart": True,
			"enableClosedCaptions": False,
			"enableLowLatency": False,
			"latencyPreference": "normal",
			"enableAutoStart": False,
			"enableAutoStop": False
		},
		"status": {
			"privacyStatus": "unlisted",
			"selfDeclaredMadeForKids": False,
		}
	}

	# Send API request
	r = requests.post('https://youtube.googleapis.com/youtube/v3/liveBroadcasts?part=snippet%2CcontentDetails%2Cstatus', headers=headers, data=json.dumps(data))

	# Debugging
	print(r.json())
	parsed_response = r.json()
	parsed_id = parsed_response['id']

	# Add thumbnail to generated livestream. Return ID.
	addthumbnail(parsed_id, '5pm-thumb.jpg', access_token)

	return parsed_id


if __name__ == '__main__':
	ACCESS_KEY = ''
	print(create10AMservice(ACCESS_KEY))