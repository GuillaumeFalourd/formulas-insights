#!/usr/bin/python3
import requests
import colorama
import csv
import os
import argparse
import json
import datetime
import sendgrid
import base64
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)

from bs4 import BeautifulSoup as soup

def run(city, profession, send_email, email_receiver):
    colorama.init()

    if [city, profession] is not None:
        try:
            response = requests.get(
                    f'https://www.linkedin.com/jobs/search?keywords={profession}&location={city}&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
                )
            response.raise_for_status()
            page_soup = soup(response.text, 'html.parser')
            return extract_job_links(profession, city, page_soup, send_email, email_receiver)
        
        except requests.HTTPError as err:
            print(colorama.Fore.RED, f'❌ Something went wrong! {err}', colorama.Style.RESET_ALL)

def extract_job_links(profession, city, cursor, send_email, email_receiver):
    job_links = []
    for res_card in cursor.findAll("li", {"class": "result-card"})[0:]:
        for links in res_card.findAll('a', {'class': 'result-card__full-card-link'})[0:]:
            job_links.append(links['href'])

    return scrape_write(profession, city, job_links, send_email, email_receiver)

def scrape_write(profession, city, links, send_email, email_receiver):
    try:
        if '-' in profession:
            formatting = [x.capitalize() for x in profession.split('-')]
            my_job = ' '.join(formatting)
        else:
            my_job = profession.capitalize()

        print(colorama.Fore.YELLOW, f'\n🕵️  There are {len(links)} available {my_job} jobs in {city.capitalize()}.\n', colorama.Style.RESET_ALL)

        current_date = datetime.datetime.now()
        current_date_format = current_date.strftime("%m-%d-%Y-%Hh%M")
        current_date_format_string = str(current_date_format)
        csv_filename = f'{my_job}_{city}_{current_date_format_string}.csv'
        
        with open(csv_filename, 'w', encoding='utf-8') as f:
            headers = ['Source', 'Organization', 'Job Title', 'Location', 'Posted', 'Applicants Hired', 'Seniority Level', 'Employment Type', 'Job Function', 'Industry']
            write = csv.writer(f, dialect='excel')
            write.writerow(headers)

            for job_link in links:
                page_req = requests.get(job_link)
                page_req.raise_for_status()

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
                        print(colorama.Fore.GREEN,
                                f'📌 {title.text}',
                                colorama.Style.RESET_ALL, 
                                colorama.Fore.YELLOW, 
                                f'- {org}', 
                                colorama.Style.RESET_ALL)
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

                write.writerows([my_data])
            
            print(colorama.Fore.YELLOW, f'\n🕵️  Written all information in: {csv_filename}', colorama.Style.RESET_ALL)
        
        check_file(csv_filename)
        
        if send_email == "yes":
            """ 
            To use SENDGRID, 
            inform RIT_SENDGRID_API_KEY and RIT_SENDGRID_EMAIL_SENDER 
            as local variables.
            """
            if os.environ.get('RIT_SENDGRID_API_KEY') is not None:
                print("\n\033[1m🤖 Sending Email...\033[0m")
                send_mail(csv_filename, my_job, city, email_receiver)
            else:
                print("\n\033[1m🤖 SENDRIG not configured...\033[0m")
                print("\n\033[1m🤖 If you want to send a message when an error occurs, add RIT_SENDGRID_API_KEY and RIT_SENDGRID_EMAIL_SENDER as local variables.\033[0m")  
    
    except requests.HTTPError as err:
        print(colorama.Fore.RED, f'❌ Something went wrong! {err}', colorama.Style.RESET_ALL)
        
def get_nums(string):
    a_list = string.split()
    for num in a_list:
        if num.isdigit():
            return num

def check_file(filename):
    for root, dirs, files in os.walk(f'{os.getcwd()}'):
        dirs = dirs
        for data in files:
            if filename == data:
                print(f"\n\033[1m✅ Successfully generated \033[4m{filename}\033[0m\033[1m file!\033[0m")


def send_mail(filename, my_job, city, email_receiver):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("RIT_SENDGRID_API_KEY"))
        from_email = os.environ.get("RIT_SENDGRID_EMAIL_SENDER")
        to_email = email_receiver.replace(',', '')
        subject = f"Linkedin: {my_job} jobs in {city} (Weekly)."
        content = f"Automated report for {my_job} jobs in {city} generated on {datetime.datetime.now()}."
        message = Mail(
            from_email = from_email,
            to_emails = to_email,
            subject = subject,
            html_content = content
        )
                                
        with open(filename, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('application/csv')
        attachment.file_name = FileName(filename)
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('')
        message.attachment = attachment
        
        response = sg.client.mail.send.post(request_body=message.get())

        print(f"\n\033[1m📩 Email sent successfully to {to_email}\033[0m")
    
    except Exception as e:
        print("Error:", e)
        print("\n\033[1m❌ An error occurred while trying to send the email!\033[0m")