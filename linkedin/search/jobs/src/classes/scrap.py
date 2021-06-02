#!/usr/bin/python3
import requests
import os
import time
import random

from bs4 import BeautifulSoup as soup

def get_datas(job, city, job_link):
    job_datas = [job_link]
    try:
        for retry in range(5):
            time.sleep(random.randint(1, 3))
            page_req = requests.get(
                url = job_link,
                headers = {'User-agent': f'{job}_{city} bot'}
                )
            if page_req.status_code == "429":
                print(f"\033[1;36m\n⚠️  Too many requests - Retrying with other IP...\033[0m")
                change_ip(random.randint(1, 30))
                time.sleep(random.randint(1, 3))
                continue
            else:
                page_req.raise_for_status()
                # Parse HTML
                job_soup = soup(page_req.text, 'html.parser')
                contents = job_soup.findAll('div', {'class': 'topcard__content-left'})[0:]
                if len(contents) == 0:
                    time.sleep(random.randint(1, 3))
                    continue
                else:
                    # Couldn't retrieve all datas for the job
                    break

        if len(contents) != 0:
            # Topcard scraping
            for content in contents:

                # Scraping Organization Names
                orgs = {'Default-Org': [org.text for org in content.findAll('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'})],
                        'Flavor-Org': [org.text for org in content.findAll('span', {'class': 'topcard__flavor'})]}

                if orgs['Default-Org'] == []:
                    org = orgs['Flavor-Org'][0]
                    job_datas.append(org)
                else:
                    for org in orgs['Default-Org']:
                        job_datas.append(org)

                # Scraping Job Title
                for title in content.findAll('h1', {'class': 'topcard__title'})[0:]:
                    print(f'\n\033[0;32m📌 {title.text}\033[0m', f'\033[1;33m- {org}\033[0m')
                    job_datas.append(title.text.replace(',', '.'))

                for location in content.findAll('span', {'class': 'topcard__flavor topcard__flavor--bullet'})[0:]:
                    job_datas.append(location.text.replace(',', '.'))

                # Scraping Job Time Posted
                posts = {'Old': [posted.text for posted in content.findAll('span', {'class': 'topcard__flavor--metadata posted-time-ago__text'})],
                        'New': [posted.text for posted in content.findAll('span', {'class': 'topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new'})]}

                if posts['New'] == []:
                    for text in posts['Old']:
                        job_datas.append(text)
                else:
                    for text in posts['New']:
                        job_datas.append(text)

                # Scraping Number of Applicants Hired
                applicants = {'More-Than': [applicant.text for applicant in content.findAll('figcaption', {'class': 'num-applicants__caption'})],
                            'Current': [applicant.text for applicant in content.findAll('span', {'class': 'topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption'})]}

                if applicants['Current'] == []:
                    for applicant in applicants['More-Than']:
                        job_datas.append(f'{get_nums(applicant)}+ Applicants')
                else:
                    for applicant in applicants['Current']:
                        job_datas.append(f'{get_nums(applicant)} Applicants')

            # Criteria scraping
            for criteria in job_soup.findAll('span', {'class': 'job-criteria__text job-criteria__text--criteria'})[:4]:
                job_datas.append(criteria.text)
        else:
            print(f"\n\033[1;36m⚠️  Saving (only) the job link on the CSV file.\033[0m")

        # print(f"\033[0;34mExtracted Datas: {job_datas} \033[0m")
        
        if len(job_datas) < 10:
            fill_number = 10 - len(job_datas)
            for i in range(0, fill_number):
                job_datas.append('')
                i += 1
                    
    except requests.HTTPError as err:
        print(f'\033[0;31m❌ Something went wrong!\033[0m', err)
        
    return job_datas

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