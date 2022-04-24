import os
import boto3
from botocore.exceptions import ClientError
from create_video import nextsunday


CHARSET = "UTF-8"


def sendemail(recipients, sender, links):

	# Create AWS email client to send emails
	client = boto3.client(
		'ses',
		region_name=os.environ["ses_aws_region"],
		aws_access_key_id=os.environ["aws_access_key_id"],
		aws_secret_access_key=os.environ["aws_secret_access_key"]
	)

	# Find the date of next sunday. Format string to dd/mm/yyyy.
	sunday = nextsunday()[0].strftime('%d/%m/%Y')

	# Backup text only email
	BODY_TEXT = (f"ETCC Service Links for {sunday}\r\n"
				f"10AM Service - {links[0]}\n"
				f"5PM Service - {links[1]}"
				)

	# Generate HTML email body with links and date
	BODY_HTML = f"""<html>
	<head></head>
	<body>
		<p>Hi Janet,<br><br>
			This is an automated email containing youtube links for this coming weeks sunday services ({sunday}).<br><br>
			<b>10AM service - <a href='{links[0]}'>{links[0]}</a><br>
			5PM service - <a href='{links[1]}'>{links[1]}</a><br><br></b>
			If there are any issues, shoot me an email and I'll try and sort it out.<br><br>
			Thanks,<br><br>
			Ethan
		</p>
	</body>
	</html>
				""" 
	# Generate subject line with date
	SUBJECT = "ETCC Service Links " + sunday

	try:
		#Provide the contents of the email.
		response = client.send_email(
			Destination={
				'ToAddresses': recipients,
			},
			Message={
				'Body': {
					'Html': {
						'Charset': CHARSET,
						'Data': BODY_HTML,
					},
					'Text': {
						'Charset': CHARSET,
						'Data': BODY_TEXT,
					},
				},
				'Subject': {
					'Charset': CHARSET,
					'Data': SUBJECT,
				},
			},
			Source=sender
		)
	# Display an error if something goes wrong.	
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		print("Email sent! Message ID:"),
		print(response['MessageId'])
