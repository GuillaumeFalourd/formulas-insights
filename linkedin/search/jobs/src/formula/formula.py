#!/usr/bin/python3
import requests
import classes.csv as csv
import classes.email as email

from bs4 import BeautifulSoup as soup

def run(city, profession, send_email, email_receiver, sendgrid_api_key, sendgrid_email_sender):
    if [city, profession] is not None:
        try:
            response = requests.get(
                    url = f'https://www.linkedin.com/jobs/search/?keywords={profession}&location={city}&position=1&pageNum=0'
                )
            response.raise_for_status()
            page_soup = soup(response.text, 'html.parser')

            # Extract Job Links
            job_links = []
            for res_card in page_soup.findAll("li", {"class": "result-card"})[0:]:
                for links in res_card.findAll('a', {'class': 'result-card__full-card-link'})[0:]:
                    job_links.append(links['href'])

            if '-' in profession:
                formatting = [x.capitalize() for x in profession.split('-')]
                job = ' '.join(formatting)
            else:
                job = profession.capitalize()

            if len(links) == 0:
                print(f"\033[1;36m\n⚠️  Couldn't extract job links list from LinkedIn, try again later!\033[0m")        
            else:
                print(f'\033[1;33m\n🕵️  There are {len(links)} available {job} jobs in {city.capitalize()}.\n\033[0m')
                
                # Extract Datas into a CSV file
                csv_filename = csv.filename(job, city)
                csv.generate_file(csv_filename, job, city, job_links)
                csv.check_file(csv_filename)
                
                print(f'\033[1;33m\n🕵️  Written all information in: {csv_filename}\033[0m')

            if send_email == "yes":
                if sendgrid_api_key is not None:
                    print("\n\033[1m🤖 Sending Email...\033[0m")
                    email.send(csv_filename, job, city, email_receiver, sendgrid_api_key, sendgrid_email_sender)
                else:
                    print("\n\033[1m🤖 SENDRIG not configured...\033[0m")
                    print("\n\033[1m🤖 If you want to send a message when an error occurs, add RIT_SENDGRID_API_KEY and RIT_SENDGRID_EMAIL_SENDER as local variables.\033[0m")  

        except requests.HTTPError as err:
            print(f'\033[0;31m❌ Something went wrong!\033[0m', err)
            
    else:
        print(f'\033[0;31m❌ Invalid Inputs. City = {city} | Profession = {profession}!\033[0m')
