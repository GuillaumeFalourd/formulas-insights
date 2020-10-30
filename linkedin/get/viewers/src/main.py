#!/usr/bin/python3
import os

from formula import formula

email = os.environ.get("LINKEDIN_EMAIL")
password = os.environ.get("LINKEDIN_PASSWORD")
formula.Run(email, password)
