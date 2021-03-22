#!/usr/bin/python3
import os

from formula import formula

url = os.environ.get("RIT_GDOC_URL")

formula.run(url)
