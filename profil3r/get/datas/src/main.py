#!/usr/bin/python3
import os

from formula import formula

fullname = os.environ.get("RIT_FULLNAME")

formula.run(fullname)
