#!/usr/bin/python3
import os

from formula import formula

city = os.environ.get("RIT_JOB_CITY")
profession = os.environ.get("RIT_JOB_TITLE")
send_email = os.environ.get("RIT_SEND_EMAIL")
email_receiver = os.environ.get("RIT_EMAIL_RECEIVER")
sendgrid_api_key = os.environ.get("RIT_SENDGRID_API_KEY")
sendgrid_email_sender = os.environ.get("RIT_SENDGRID_EMAIL_SENDER")

formula.run(city, profession, send_email, email_receiver, sendgrid_api_key, sendgrid_email_sender)
