#!/usr/bin/python3
import requests
import os
import time

from bs4 import BeautifulSoup as soup

def get_datas(job, city, job_link):
    for retry in range(5):
        time.sleep(5)
        page_req = requests.get(
            url = job_link,
            headers = {'User-agent': f'{job}_{city} bot'}
            )
        if page_req.status_code == "429":
            change_ip(random.randint(1, 30))
            time.sleep(3)
            continue
        else:
            page_req.raise_for_status()
            break

    # Parse HTML
    job_soup = soup(page_req.text, 'html.parser')
    my_data = [job_link]

    # Topcard scraping
    for content in job_soup.findAll('div', {'class': 'topcard__content-left'})[0:]:

        # Scraping Organization Names
        orgs = {'Default-Org': [org.text for org in content.findAll('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'})],
                'Flavor-Org': [org.text for org in content.findAll('span', {'class': 'topcard__flavor'})]}

        if orgs['Default-Org'] == []:
            org = orgs['Flavor-Org'][0]
            my_data.append(org)
        else:
            for org in orgs['Default-Org']:
                my_data.append(org)

        # Scraping Job Title
        for title in content.findAll('h1', {'class': 'topcard__title'})[0:]:
            print(f'\033[0;32m📌 {title.text}\033[0m', f'\033[1;33m- {org}\033[0m')
            my_data.append(title.text.replace(',', '.'))

        for location in content.findAll('span', {'class': 'topcard__flavor topcard__flavor--bullet'})[0:]:
            my_data.append(location.text.replace(',', '.'))

        # Scraping Job Time Posted
        posts = {'Old': [posted.text for posted in content.findAll('span', {'class': 'topcard__flavor--metadata posted-time-ago__text'})],
                'New': [posted.text for posted in content.findAll('span', {'class': 'topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new'})]}

        if posts['New'] == []:
            for text in posts['Old']:
                my_data.append(text)
        else:
            for text in posts['New']:
                my_data.append(text)

        # Scraping Number of Applicants Hired
        applicants = {'More-Than': [applicant.text for applicant in content.findAll('figcaption', {'class': 'num-applicants__caption'})],
                    'Current': [applicant.text for applicant in content.findAll('span', {'class': 'topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption'})]}

        if applicants['Current'] == []:
            for applicant in applicants['More-Than']:
                my_data.append(f'{get_nums(applicant)}+ Applicants')
        else:
            for applicant in applicants['Current']:
                my_data.append(f'{get_nums(applicant)} Applicants')

    # Criteria scraping
    for criteria in job_soup.findAll('span', {'class': 'job-criteria__text job-criteria__text--criteria'})[:4]:
        my_data.append(criteria.text)

    print("Datas:", my_data)
    return my_data

def get_nums(string):
    a_list = string.split()
    for num in a_list:
        if num.isdigit():
            return num

def change_ip(number):
    print("Current IP Address")
    os.system('sudo hostname -I')
    os.system('sudo ifconfig eth0 down')
    os.system(f'sudo ifconfig eth0 192.168.1.{number}')
    os.system('sudo ifconfig eth0 up')
    print("New IP Address")
    os.system('sudo hostname -I')