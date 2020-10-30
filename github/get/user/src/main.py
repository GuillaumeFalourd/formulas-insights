#!/usr/bin/python3
import os

from formula import formula

username = os.environ.get("GITHUB_USERNAME")
repo_details = os.environ.get("REPO_DETAILS")
keep_file = os.environ.get("KEEP_FILE")

formula.Run(username, repo_details, keep_file)
