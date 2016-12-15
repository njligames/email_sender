import send
import logging
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http

logger = logging.getLogger(__name__)

def gmailSendEmail(flags, message_subject, message_text, message_to_email):
	SCOPES = 'https://www.googleapis.com/auth/gmail.compose' # 1 or more scopes, i.e., 'https://www.googleapis.com/auth/youtube'
	CLIENT_SECRET_FILE = 'client_secret.json' # downloaded JSON file

	# store = file.Storage('storage.json')
	store = file.Storage('gmail.storage')

	creds = store.get()
	if not creds or creds.invalid:
	  flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
	  if flags:
	    creds = tools.run_flow(flow, store, flags)
	  else:
	    creds = tools.run(flow, store)

	# API information, i.e., (API='youtube', VERSION='v3')
	SERVICE = build('gmail', 'v1', http=creds.authorize(Http()))

	logger.info('Sending Message %s', message_to_email)

	# message_text = "<b>This is HTML message.</b><br/><h1>This is headline.</h1>"
	# message_subject = "JAMES"

	try:
		# print("%s, %s, %s, %s" % (message_subject, message_text, message_to_email, str(dir(SERVICE))))

		body = send.CreateMessage(message_to_email, message_subject, message_text)
		message = (SERVICE.users().messages().send(userId="me", body=body).execute())
		print('Message : %s' % message)
	except Exception as error:
		print('An error occurred: %s' % error)