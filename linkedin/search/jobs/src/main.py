#!/usr/bin/python3
import os

from formula import formula

city = os.environ.get("RIT_JOB_CITY")
profession = os.environ.get("RIT_JOB_TITLE")
send_email = os.environ.get("RIT_SEND_EMAIL")
email_receiver = os.environ.get("RIT_EMAIL_RECEIVER")

formula.run(city, profession, send_email, email_receiver)
