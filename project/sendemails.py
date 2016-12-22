#!/usr/bin/python
# -*- coding: latin-1 -*-
#title			:sendemails.py
#description	:Utility to send a mass amount of emails.
#author			:James Folk
#date			:20161216
#version		:v1.0.0
#usage			:python sendemails.py
#notes			:
#python_version	:2.6.6
#==============================================================================


from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
import time
import logging
import os
from functools import partial
from multiprocessing.pool import Pool
from multiprocessing import Value
import emailutility
from apiclient.discovery import build

logger = logging.getLogger(__name__)

quota_count = None
quota_start_time = time.time()
quota_unit_cost = 100

try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

message_subject = "Student Loan, HELP!?"
emails=["gafolk@hotmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com"]

f = open('message.html', 'r')
message_text = f.read()

def gmailSendEmail(flags, message_subject, message_text, message_to_email):
    global quota_count
    global quota_start_time
    global quota_unit_cost

    SCOPES = 'https://www.googleapis.com/auth/gmail.compose' # 1 or more scopes, i.e., 'https://www.googleapis.com/auth/youtube'
    CLIENT_SECRET_FILE = 'client_secret.json' # downloaded JSON file
    #CLIENT_SECRET_FILE = 'Unknown-2' # downloaded JSON file

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

    try:
            body = emailutility.CreateMessage(message_to_email, message_subject, message_text)
            message = (SERVICE.users().messages().send(userId="me", body=body).execute())
            with quota_count.get_lock():
                quota_count.value += quota_unit_cost
            print('Message : %s, %f' % (message, quota_count.value))
    except Exception as error:
            print('An error occurred: %s' % error)


def multi(flags, emails):

  start = time.time()

  mail = partial(gmailSendEmail, flags, message_subject, message_text)
  pool = Pool(processes=8)
  #pool.map_async(mail, emails)
  pool.map(mail, emails)
  pool.terminate()

  end = time.time()

  print("multi process performed %s emails which took %s seconds" % (str(len(emails)), str(end - start)))

quota_count = Value('i', 0)
multi(flags, emails)

#for email in emails:
    #gmailSendEmail(flags, message_subject, message_text, email)
