#!/usr/bin/env python3

import os
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

def Run(user, key, contribution):
    repos_url = f"https://api.github.com/users/{user}/repos"
    repo_names = [repo["name"] for repo in requests.get(repos_url).json()]
    insights = []
    base_url = f"https://api.github.com/repos/{user}/"

    print(f"🐙 Getting insights for {user}'s repos:")
    for repo in repo_names:
         print(f"\t- github.com/ZupIT/{repo}/")
        repo_url_zup = urljoin(base_url_zup, repo + "/")
        traffic = requests.get(
            urljoin(repo_url_zup, "traffic/views",), auth=HTTPBasicAuth(user, key),
        ).json()

        clones = requests.get(
            urljoin(repo_url_zup, "traffic/clones",), auth=HTTPBasicAuth(user, key),
        ).json()

        contributors = requests.get(
            urljoin(repo_url_zup, "contributors",), auth=HTTPBasicAuth(user, key),
        ).json()

        url = f"https://api.github.com/repos/ZupIT/{repo}"
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
            stars = "-"

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
        for insight in insights:
            print(f"\nRepository: https://github.com/{user}/" + insight["repo"] + "/")
            print("---------------------------------------------")
            print(f'{"Github ID":10} {"Username":^20} {"Contributions":^10}')
            print("---------------------------------------------")
            for contributor in insight["contributors_list"]:
                print(
                f'{contributor["id"]:^10} {contributor["login"]:^20} {contributor["contributions"]:^10}'
                )
