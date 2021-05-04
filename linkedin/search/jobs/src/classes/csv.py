#!/usr/bin/python3
import requests
import csv
import os
import datetime
import time

import classes.scrap as scrap

def filename(job, city):
    # Create filename according to inputs and date
    current_date = datetime.datetime.now()
    current_date_format = current_date.strftime("%m-%d-%Y-%Hh%M")
    current_date_format_string = str(current_date_format)
    filename = f'{job.replace(" ", "_")}_{city.replace(" ", "_")}_{current_date_format_string}.csv'
    return filename

def generate_file(csv_filename, job, city, links):
    with open(csv_filename, 'w', encoding='utf-8') as f:
        headers = ['Source', 'Organization', 'Job Title', 'Location', 'Posted', 'Applicants Hired', 'Seniority Level', 'Employment Type', 'Job Function', 'Industry']
        write = csv.writer(f, dialect='excel')
        write.writerow(headers)
        
        for job_link in links:
            job_datas = scrap.get_datas(job, city, job_link)
            write.writerows([job_datas])

def check_file(filename):
    for root, dirs, files in os.walk(f'{os.getcwd()}'):
        dirs = dirs
        for data in files:
            if filename == data:
                print(f"\n\033[1m✅ Successfully generated \033[4m{filename}\033[0m\033[1m file!\033[0m")
