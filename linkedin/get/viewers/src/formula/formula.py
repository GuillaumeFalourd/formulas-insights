#!/usr/bin/python3
from colored import fg, attr

import requests
from bs4 import BeautifulSoup
import re
import getpass
import sys

def Run(email, password):
    # Leverage session of requests module
    client = requests.Session()

    HOMEPAGE_URL = 'https://www.linkedin.com'
    LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
    PROFILE_VIEWS_URL = 'https://www.linkedin.com/me/profile-views/urn:li:wvmp:summary/'

    # It is to get loginCsrfParam value which is needed while logging in
    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, "html.parser")
    csrf = soup.find('input', {'name': 'loginCsrfParam'}).get('value')

    # Building the payload to login
    login_information = {
        'session_key': email,
        'session_password': password,
        'loginCsrfParam': csrf,
        'trk': 'guest_homepage-basic_sign-in-submit'
    }

    # Login with login_information data
    client.post(LOGIN_URL, data=login_information)

    # Get the content from profile views summary page
    profile_views_raw = client.get(PROFILE_VIEWS_URL).content

    process_and_print(profile_views_raw)
    return None

def process_and_print(raw_data):
    # Get raw content in html format
    profile_views_html = BeautifulSoup(raw_data, "html.parser")

    # look for <code id="bpr-guid-" and get the value
    code = profile_views_html.findAll('code', {'id': re.compile('^bpr-guid-')})

    if not code:
        exit("Possible wrong creds or data. Please check creds or contents and retry\n")

    final_viewer_list = []

    for line in code:
        string_line = str(line)
        profile_search = re.findall('"firstName":"(\w+\s?\w+?)","lastName":"([a-zA-z-,\.\s]+)"', string_line)
        if profile_search :
            final_viewer_list.extend(profile_search)

    # using join() + map(), joining tuple elements
    viewer_name_list = list(map(" ".join, final_viewer_list))

    # unique values in list
    viewer_name_list = list(set(viewer_name_list))

    # sort the name list, case insensitive sorting
    viewer_name_list.sort(key=lambda v: v.upper())

    print("{} viewers have visited your LinkedIn profile today\n".format(len(viewer_name_list)))

    count = 0

    # printing nicely the viewer lists
    for fullname in viewer_name_list:
        count += 1
        print(str(count) + ". " + fullname)

    return None