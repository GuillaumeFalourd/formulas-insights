#!/usr/bin/env python3

import os
import re

from urllib.parse import urljoin

import requests
from requests import get
from requests.auth import HTTPBasicAuth

import json

regex_pattern = r"(?<=\+)(.*)"

def Run(user, key, contribution):
    repos_url = f"https://api.github.com/users/{user}/repos"
    repo_names = [repo["name"] for repo in requests.get(repos_url).json()]
    insights = []
    base_url = f"https://api.github.com/repos/{user}/"

    print(f"🐙 Getting insights for {user}'s repos:")
    for repo in repo_names:
        print(f"\t- github.com/{user}/{repo}/")
        repo_url = urljoin(base_url, repo + "/")
        traffic = requests.get(
            urljoin(repo_url, "traffic/views",), auth=HTTPBasicAuth(user, key),
        ).json()

        clones = requests.get(
            urljoin(repo_url, "traffic/clones",), auth=HTTPBasicAuth(user, key),
        ).json()

        contributors = requests.get(
            urljoin(repo_url, "contributors",), auth=HTTPBasicAuth(user, key),
        ).json()

        url = f"https://api.github.com/repos/{user}/{repo}"
        repo_stats = requests.get(
            url, auth=HTTPBasicAuth(user, key),
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
                "repo": repo,
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

    print("\n-------------------------------------------------------------------------------------------------------")
    print(f'{"Repository":25} {"Views":^10} {"Uniques":^10} {"Clones":^10} {"Contributors":^10} {"Forks":^10} {"Stars":^10} {"Watchers":^10}')
    print("-------------------------------------------------------------------------------------------------------")
    for insight in insights:
        print(
            f'{insight["repo"]:25} {insight["views"]:^10} {insight["uniques"]:^10} {insight["clones"]:^10} {insight["contributors"]:^12} {insight["forks"]:^10} {insight["stars"]:^10} {insight["watchers"]:^10}'
        )

    if contribution == "yes" :
        print_contribution(insights, user, key)

def print_contribution(insights, user, key):
    for insight in insights:
            print(f"\nRepository: https://github.com/{user}}/" + insight["repo"] + "/")
            print("----------------------------------------------------------------------------------------------------------------------------")
            print(f'{"Github ID":10} {"Username":^20} {"Name":^35} {"Email":^40} {"Contributions":^10}')
            print("----------------------------------------------------------------------------------------------------------------------------")

            try:
                for contributor in insight["contributors_list"]:
                    get_contributor_details(user, key, contributor)

                    print(
                        f'{contributor["id"]:^10} {contributor["login"]:^20} {contributor["name"]:^35} {contributor["email"]:^40} {contributor["contributions"]:^10}'
                    )

            except(TypeError):
                print("🚫 Sorry: We could't retrieve the contributors list for this repository...\n")

def get_contributor_details(user, key, contributor):
    events = requests.get(
        ('https://api.github.com/users/%s/events?per_page=100' % (contributor["login"])), auth=HTTPBasicAuth(user, key),
    ).json()

    github_user = requests.get(
        ('https://api.github.com/users/%s' % (contributor["login"])), auth=HTTPBasicAuth(user, key),
    ).json()

    contributor["name"] = github_user["name"]

    got_verified_email = get_github_datas(events, contributor)

    check_email_and_name_datas(contributor)

    if not got_verified_email and contributor["email"] == "-" or contributor["name"] == "-" or contributor["name"] == contributor["login"]:
        extract_undefined_datas(events, contributor)

def get_github_datas(events, contributor):
    got_verified_email = False
    for event in events:
        if not got_verified_email and event["type"] == "PushEvent" and event["payload"] is not None:
            payload = event["payload"]
            for commit in payload["commits"]:
                if commit["author"] is not None:
                    author = commit["author"]
                    try:
                        if author["name"] in contributor["name"] and "github" not in author["email"]:
                            contributor["email"] = author["email"]
                            got_verified_email = True

                        if contributor["email"] is not None and author["name"] in contributor["login"] and "github" not in author["email"]:
                            contributor["email"] = author["email"]
                            got_verified_email = True

                    except (KeyError, TypeError):
                        if author["name"] in (contributor["login"], contributor["name"]) and "github" not in author["email"]:
                            contributor["email"] = author["email"]

    return got_verified_email

def check_email_and_name_datas(contributor):
    try:
        if contributor["name"] is None:
            contributor["name"] = "-"
    except (IndexError, TypeError, KeyError):
        contributor["name"] = "-"

    try:
        if contributor["email"] is None:
            contributor["email"] = "-"
    except (IndexError, TypeError, KeyError):
        contributor["email"] = "-"

def extract_undefined_datas(events, contributor):
        for event in events:
            if event["type"] == "PushEvent" and event["payload"] is not None and event["actor"] is not None:
                actor = event["actor"]
                payload = event["payload"]
                if actor["login"] == contributor["login"]:
                    for commit in payload["commits"]:
                        if commit["author"] is not None:
                            author = commit["author"]
                            try:
                                if contributor["email"] == "-" and "github" not in author["email"] :
                                        contributor["email"] = author["email"]

                            except (KeyError, TypeError):
                                contributor["email"] = "-"

                            if contributor["name"] == "-" or contributor["name"] == contributor["login"]:
                                contributor["name"] = author["name"]

def get_contributor_email(event, contributor):
    if event["type"] == "PushEvent" and event["payload"] is not None:
        payload = event["payload"]
        for commit in payload["commits"]:
            if commit["author"] is not None:
                author = commit["author"]
                contributor["email"] = author["email"]
