import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client


app = flask.Flask(__name__)


@app.route('/')
def index():
  return flask.redirect(flask.url_for('static', filename='oauth2callback'))

  return flask.redirect(flask.url_for('static', filename='oauth2callback'))

  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('static', filename='oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('static', filename='oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    # drive_service = discovery.build('drive', 'v2', http_auth)
    # files = drive_service.files().list().execute()

    try:
      message = (service.users().messages().send(userId='me', body="message").execute())
      print 'Message Id: %s' % message['id']
      return json.dumps(message)
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      return json.dumps(error)


@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/drive.metadata.readonly',
      redirect_uri=flask.url_for('static', filename='oauth2callback', _external=True),
      include_granted_scopes=True)
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('static', filename='index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()