from bs4 import BeautifulSoup
import requests
import requests.exceptions
# from urllib.parse import urlsplit
from urlparse import urlparse, urlsplit
from collections import deque
import re

import sqlite3

import lepl.apps.rfc3696
email_validator = lepl.apps.rfc3696.Email()

def crawl(tbl):

    database = tbl[0]
    new_urls = tbl[1]

    conn = sqlite3.connect(database)

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    emails = set()

    # process urls one by one until we exhaust the queue
    while len(new_urls):

        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        #print("base_url %s" % base_url)
        #print("path %s" % path)

        # get url's content
        print("(%s) - Processing %s" % (database, url))
        try:
            response = requests.get(url)
            response_text = response.text.encode('utf-8', 'ignore')

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL, requests.exceptions.ContentDecodingError):
            # ignore pages with errors
            continue

        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(r'[\w\.-]+@[\w\.-]+', response_text, re.I))

        ok = False
        for email in new_emails:
            if email_validator(email):
                # if re.match(r"\w+@\d{1,}x\w+.png", email, flags=0):
                if not re.match(r'([-\w@]+\.(?:jpg|gif|png))', email, flags=0):
                    cursor = conn.execute("INSERT OR IGNORE INTO EMAIL (EMAIL) VALUES (\'" + email + "\');")

        
        conn.commit()

        cursor = conn.execute("SELECT COUNT(*) from EMAIL")
        result = cursor.fetchone()
        print("\t\t(%s) - Number of Rows %d" % (database, result[0]))

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response_text, "html.parser")

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link

            if not link.startswith('http://ftp'):
                # add the new url to the queue if it was not enqueued nor processed yet
                if not link in new_urls and not link in processed_urls:
                    new_urls.append(link)

    conn.close()

emailParams = ['emails.db', deque(['http://www.themoscowtimes.com/contact_us/index.php'])]
cancerParams = ['braincancer.db', deque(['https://www.reddit.com/r/braincancer', 'https://www.reddit.com/r/cancer', 'https://www.reddit.com/r/SuicideWatch'])]
libraryParams = ['library.db', deque(['https://www.reddit.com/r/Libraries', 'https://www.reddit.com/r/Teachers', 'https://www.reddit.com/r/POLITIC'])]

params = [emailParams, cancerParams, libraryParams]

from multiprocessing.pool import Pool

pool = Pool(processes=8)

pool.map(crawl, params)
pool.terminate()

