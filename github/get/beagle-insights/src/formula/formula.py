#!/usr/bin/env python3

import os
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

def Run(user, key, contribution):
    repos_url_zup = f"https://api.github.com/users/ZupIT/repos"
    repo_names_zup = ["beagle", "beagle-web-react", "beagle-web-core", "beagle-web-angular"]
    
    insights = []
    contributors = []
    base_url_zup = f"https://api.github.com/repos/ZupIT/"

    print(f"🐙 Getting insights for ZupIT's repos:")
    for repo in repo_names_zup:
        print(f"\t- github.com/ZupIT/{repo}/")
        repo_url_zup = urljoin(base_url_zup, repo + "/")
        traffic = requests.get(
            urljoin(repo_url_zup, "traffic/views",), auth=HTTPBasicAuth(user, key),
        ).json()

        clones = requests.get(
            urljoin(repo_url_zup, "traffic/clones",), auth=HTTPBasicAuth(user, key),
        ).json()["count"]

        contributors = requests.get(
            urljoin(repo_url_zup, "contributors",), auth=HTTPBasicAuth(user, key),
        ).json()

        url = f"https://api.github.com/search/repositories?q=user%3AZupIT+repo%3A{repo}+{repo}"
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

    print("\n-------------------------------------------------------------------------------------------")
    print(f'{"Repository":25} {"Views":^10} {"Uniques":^10} {"Clones":^10} {"Contributors":^10} {"Forks":^10} {"Stars":^10}')
    print("-------------------------------------------------------------------------------------------")
    for insight in insights:
        print(
            f'{insight["repo"]:25} {insight["views"]:^10} {insight["uniques"]:^10} {insight["clones"]:^10} {insight["contributors"]:^12} {insight["forks"]:^10} {insight["stars"]:^10}'
        )
    if contribution == "yes" :
        for insight in insights:
            print("\nRepository: https://github.com/ZupIT/" + insight["repo"] + "/")
            print("---------------------------------------------")
            print(f'{"Github ID":10} {"Username":^20} {"Contributions":^10}')
            print("---------------------------------------------")
            for contributor in insight["contributors_list"]:
                print(
                f'{contributor["id"]:^10} {contributor["login"]:^20} {contributor["contributions"]:^10}'
                )