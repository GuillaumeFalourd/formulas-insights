# Formulas Insights

![title](https://user-images.githubusercontent.com/22433243/119176109-11d8e600-ba41-11eb-8ed7-c917ab061e56.png)

## 📚 Documentation

This repository contains Ritchie formulas which can be executed by [ritchie-cli](https://github.com/ZupIT/ritchie-cli).

- [Ritchie CLI documentation](https://docs.ritchiecli.io)

## 🔎 What you'll find in this repository

![Demo Github](/docs/img/rit-github-insights.png)

***

![Demo Github](/docs/img/rit-github-get-user.png)

***

![Demo LinkedIn Viewers](/docs/img/rit-linkedin-get-viewers.png)

***

![Demo Linkedin Jobs](/docs/img/rit-linkedin-search-jobs.png)

***

![Demo Google Docs](/docs/img/rit-googledoc-get-insights.png)

***

![Demo Profil3r 1.3.3](/docs/img/rit-profil3r-get-datas.png)

## 📦 Use Formulas

To import this repository, you need [Ritchie CLI installed](https://docs.ritchiecli.io/getting-started/installation)

Then, you can use the `rit add repo` command manually, or execute the command line below directly on your terminal (since CLI version 2.8.0):

```bash
rit add repo --provider="Github" --name="formulas-insights" --repoUrl="https://github.com/GuillaumeFalourd/formulas-insights" --priority=1
```

Finally, you can check if the repository has been imported correctly by executing the `rit list repo` command.

## ♻️ Contribute to the repository

### 🆕 Creating formulas

1. Fork and clone the repository
2. Create a branch: `git checkout -b <branch_name>`
3. Check the step by step of [how to create formulas on Ritchie](https://docs.ritchiecli.io/tutorials/formulas/how-to-create-formulas)
4. Add your formulas to the repository
and commit your implementation: `git commit -m '<commit_message>`
5. Push your branch: `git push origin <project_name>/<location>`
6. Open a pull request on the repository for analysis.

### 🆒 Updating Formulas

1. Fork and clone the repository
2. Create a branch: `git checkout -b <branch_name>`
3. Add the cloned repository to your workspaces (`rit add workspace`) with a highest priority (for example: 1).
4. Check the step by step of [how to implement formulas on Ritchie](https://docs.ritchiecli.io/tutorials/formulas/how-to-implement-a-formula)
and commit your implementation: `git commit -m '<commit_message>`
5. Push your branch: `git push origin <project_name>/<location>`
6. Open a pull request on the repository for analysis.

- [Contribute to Ritchie community](https://github.com/ZupIT/ritchie-formulas/blob/master/CONTRIBUTING.md)

