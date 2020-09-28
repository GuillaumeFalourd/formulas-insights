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

    print(f"🐙 Getting traffic insights for {user}'s repos:")
    for repo in repo_names:
        print(f"\t- github.com/{user}/{repo}/")
        repo_url = urljoin(base_url, repo + "/")
        traffic = requests.get(
            urljoin(repo_url, "traffic/views",), auth=HTTPBasicAuth(user, key),
        ).json()

        clones = requests.get(
            urljoin(repo_url, "traffic/clones",), auth=HTTPBasicAuth(user, key),
        ).json()["count"]

        contributors = requests.get(
            urljoin(repo_url, "contributors",), auth=HTTPBasicAuth(user, key),
        ).json()

        url = f"https://api.github.com/search/repositories?q=user%3A{user}+repo%3A{repo}+{repo}"
        repo_stats = requests.get( 
            url, auth=HTTPBasicAuth(user, key), 
        ).json()

        try:
            forks = repo_stats["items"][0]["forks_count"]
        except IndexError:
            forks = "-"

        try:
            stars = repo_stats["items"][0]["stargazers_count"]
        except IndexError:
            stars = "-"  

        insights.append(
            {
                "repo": repo,
                "views": traffic["count"],
                "uniques": traffic["uniques"],
                "clones": clones,
                "contributors": len(contributors),
                "contributors_list": contributors,
                "forks": forks,
                "stars": stars,
            }
        )

    print("\n---------------------------------------------------------------------------------------------")
    print(f'{"Repository":25} {"Views":^10} {"Uniques":^10} {"Clones":^10} {"Contributors":^10} {"Forks":^10} {"Stars":^10}')
    print("---------------------------------------------------------------------------------------------")
    for insight in insights:
        print(
            f'{insight["repo"]:25} {insight["views"]:^10} {insight["uniques"]:^10} {insight["clones"]:^10} {insight["contributors"]:^12} {insight["forks"]:^10} {insight["stars"]:^10}'
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
