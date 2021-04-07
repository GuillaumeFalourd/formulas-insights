#!/usr/bin/python3
import os

from formula import formula

city = os.environ.get("RIT_JOB_CITY")
profession = os.environ.get("RIT_JOB_TITLE")

formula.run(city, profession)
