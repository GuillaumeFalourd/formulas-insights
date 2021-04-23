#!/usr/bin/python3
import datetime
import inquirer
import requests
import re
import csv
import os
import json

repositories = [
    "beagle",
    "beagle-web-react",
    "beagle-web-core",
    "beagle-web-angular",
    "charlescd",
    "charlescd-docs",
    "horusec",
    "horusec-engine-docs",
    "ritchie-cli",
    "ritchie-formulas",
    "ritchie-formulas-demo"
    ]

def run(token):
    
    insights = []

    authorization = f"token {token}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization" : authorization,
        }

    for repository in repositories:
        repo_url = f"https://api.github.com/repos/ZupIT/{repository}"

        print(f"🐙 Getting insights for ZupIT's \033[36m{repository}\033[0m repository.")

        traffic = requests.get(
            url = repo_url + "/traffic/views",
            headers = headers,
        ).json()

        clones = requests.get(
            url = repo_url + "/traffic/clones",
            headers = headers,
        ).json()

        contributors = requests.get(
            url = repo_url + "/contributors",
            headers = headers,
        ).json()

        repo_stats = requests.get(
            url = repo_url,
            headers = headers,
        ).json()

        try:
            clones = clones["count"]
        except (IndexError, KeyError) :
            clones = "-"

        try:
            forks = repo_stats["forks_count"]
        except (IndexError, KeyError):
            forks = "-"

        try:
            stars = repo_stats["stargazers_count"]
        except (IndexError, KeyError):
            stars = "-"

        try:
            watchers = repo_stats["subscribers_count"]
        except (IndexError, KeyError):
            watchers = "-"

        try:
            views = traffic["count"]
        except (IndexError, KeyError):
            views = "-"

        try:
            uniques = traffic["uniques"]
        except (IndexError, KeyError):
            uniques = "-"

        insights.append(
            {
                "repo": repository,
                "views": views,
                "uniques": uniques,
                "clones": clones,
                "contributors": len(contributors),
                "contributors_list": contributors,
                "forks": forks,
                "stars": stars,
                "watchers": watchers,
            }
        )

    create_csv_file(insights)


def get_repositories(url, headers):
    result = []
    r = requests.get(
        url = url,
        headers = headers
        )

    if "next" in r.links :
        result += get_repositories(r.links["next"]["url"], headers)

    for data in r.json():
        result.append(data["name"])

    return result


def create_csv_file(insights):
    current_date = datetime.datetime.now()
    current_date_format = current_date.strftime("%m-%d-%Y-%Hh%M")
    current_date_format_string = str(current_date_format)
    filename = "zup-insights-" + current_date_format_string + ".csv"

    file = open(filename, 'w+', newline ='')
    with file:
        header = ["Repository", "Views (14d)", "Uniques (14d)", "Clones (14d)", "Contributors", "Forks", "Stars", "Watchers"]
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()

    file = open(filename, 'a+', newline ='')
    with file:
        for insight in insights:
            data = [[insight["repo"], insight["views"], insight["uniques"], insight["clones"], insight["contributors"], insight["forks"], insight["stars"], insight["watchers"]]]
            write = csv.writer(file)
            write.writerows(data)

    print(f"\n\033[1m✅ Successfully generated \033[4m{filename}\033[0m\033[1m file for ZupIT's repositories\033[0m")
