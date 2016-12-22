from httplib2 import Http
from oauth2client import file, client, tools

from email.mime.text import MIMEText
import base64
import time
from redis import Redis, StrictRedis
from rq import Queue
from rq import get_current_job
from rq.job import Job


import logging
import os
from functools import partial
from multiprocessing.pool import Pool
# from time import time

try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

message_text = "<html><header><title>This is title</title></header><body>Hello world</body></html>"
message_subject = "I love you Natasha"
email = "jamesfolk1@gmail.com"

emails=["jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com", "jamesfolk1@gmail.com"]

from gmailSend import gmailSendEmail

def redis(flags, emails):
  redis_conn = StrictRedis(host='pub-redis-10320.us-east-1-3.7.ec2.redislabs.com', port=10320, db=0, password='1Password$', socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
  q = Queue(connection=redis_conn)

  jobs = []
  for email in emails:
    jobs.append(q.enqueue_call(func=gmailSendEmail, args=(flags, message_subject, message_text, email, )))

  start = time.time()
  for job in jobs:
    job.perform()
  end = time.time()

  print("redis process performed %s emails which took %s seconds" % (str(len(emails)), str(end - start)))

def multi(flags, emails):

  mail = partial(gmailSendEmail, flags, message_subject, message_text)

  pool = Pool(processes=8)

  start = time.time()
  pool.map(mail, emails)
  pool.terminate()
  end = time.time()

  print("multi process performed %s emails which took %s seconds" % (str(len(emails)), str(end - start)))

#redis(flags, emails)
multi(flags, emails)
#gmailSendEmail(flags, message_subject, message_text, "jamesfolk1@gmail.com")
#Quota: https://developers.google.com/gmail/api/v1/reference/quota

