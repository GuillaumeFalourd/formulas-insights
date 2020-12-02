# Ritchie Formulas Repository - Insights

![Rit banner](/docs/img/ritchie-banner.png)

## Documentation

[Contribute to the Ritchie community](https://github.com/ZupIT/ritchie-formulas/blob/master/CONTRIBUTING.md)

This repository contains rit formulas which can be executed by the [ritchie-cli](https://github.com/ZupIT/ritchie-cli).

- [Gitbook](https://docs.ritchiecli.io)

## Use Formulas

To import this repository, you need to have [Ritchie CLI installed](https://docs.ritchiecli.io/getting-started/installation)

Then, you can use the `rit add repo` command manually, or execute the command line below directly on your terminal:

```bash
echo '{"provider":"Github", "name":"insights", "url":"https://github.com/GuillaumeFalourd/formulas-insights", "priority":1}' | rit add repo --stdin
```

Finally, you can check if the repository has been imported correctly by executing the `rit list repo` command.

## Samples execution

![Demo Github](/docs/img/rit-github-insights.png)

= = = = = = = = = = = = = = = = = = = = = = = = = = = = =

![Demo Github](/docs/img/rit-github-get-user.png)

= = = = = = = = = = = = = = = = = = = = = = = = = = = = =

![Demo LinkedIn](/docs/img/rit-linkedin-get-viewers.png)

## Build and test formulas locally

```bash rit build formula```

## Contribute to the repository with your formulas

1. Fork the repository
2. Create a branch: `git checkout -b <branch_name>`
3. Check the step by step of [how to create formulas on Ritchie](https://docs.ritchiecli.io/getting-started/creating-formulas)
4. Add your formulas to the repository
and commit your implementation: `git commit -m '<commit_message>`
5. Push your branch: `git push origin <project_name>/<location>`
6. Open a pull request on the repository for analysis.
