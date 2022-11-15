# Contributing

Contributions to ebau-gwr are very welcome! Best have a look at the open [issues](https://github.com/inosca/ebau-gwr)
and open a [GitHub pull request](https://github.com/inosca/ebau-gwr/compare). See instructions below how to setup development
environment. Before writing any code, best discuss your proposed change in a GitHub issue to see if the proposed change makes sense for the project.

## Setup development environment

### Clone

To work on ebau-gwr you first need to clone

```bash
git clone https://github.com/inosca/ebau-gwr.git
cd ebau-gwr
```

### Open Shell

Once it is cloned you can easily open a shell in the docker container to
open an development environment.

```bash
# needed for permission handling
# only needs to be run once
echo UID=$UID > .env
# open shell
docker-compose run --rm ebau-gwr bash
```

### Testing

Once you have shelled in docker container as described above
you can use common python tooling for formatting, linting, testing
etc.

```bash
# linting
flake8
# format code
black .
# running tests
pytest
# create migrations
./manage.py makemigrations
# install debugger or other temporary dependencies
pip install --user pdbpp
```

Writing of code can still happen outside the docker container of course.

### Install new requirements

In case you're adding new requirements you simply need to build the docker container
again for those to be installed and re-open shell.

```bash
docker-compose build --pull
```

### Setup pre commit

Pre commit hooks is an additional option instead of executing checks in your editor of choice.

First create a virtualenv with the tool of your choice before running below commands:

```bash
pip install pre-commit
pip install -r requiements-dev.txt -U
pre-commit install
```

## Release
1. Pull the up to date `main` branch locally

1. Update the remote

   ```bash
   git fetch [insert your upstream/origin name]
   ```

1. Get the new version

   ```bash
   semantic-release version --noop -D version_source=tag
   ```

1. Update the line `version = "x.x.x"` with your new version in `pyproject.toml`

1. Now generate the change-log

   ```bash
   semantic-release changelog --noop --unreleased -D version_source=tag
   ```

1. Append the generated change log with your version at the top of `CHANGELOG.md`

1. Create a pull request with these changes

1. Once merged in main, pull the upstream/origin main again

1. Create a git tag with the following format: `vx.x.x` where `x.x.x` is the previously generated version number

    ```bash
    git tag -a vx.x.x
    ```

10. The previous command will open a text editor to annotate the tag. Insert the previously generated change-log and save

11. Push the tag to upstream

    ```bash
    git push [origin/upstream] vx.x.x
    ```
