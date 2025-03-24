# 2024 Team SH20 Project

## Members

- 2840506 Heng Zhen Yao
- 2777042 Levack Fraser Wiremu
- 2802089 Tee Zhi Xi
- 2618972 McIntyre Aaron
- 2768903 Nelson Freddie

## Requirements

- python 3.12
- django 5.1.2

## Contributing

Commit messages should follow the guidelines described [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

Once you have cloned the repository, you can run the `setup.ps1` script setup python and it's dependencies, as well as pre-commit hooks.

```powershell
.\scripts\setup.ps1
```

The python virtual environment will be created in `C:\Users\Public\sh20-main-venv`, it will be automatically activated by the setup script. However you can also activate it using:

```powershell
.\scripts\activate-venv.ps1
```

And deactivate it using:

```powershell
deactivate
```

All code is ran through the black formatter, and the flake8 linter by the pre-commit hooks. The pre-commit hooks will run these checks before allowing you to commit. You may also run these tools from the command line using:

```powershell
black .
```

```powershell
flake8 .
```

You are now ready to start developing!

## Running our Project Locally

1. Clone from the git repository to your system

2. Go to Project Root Directory and make sure you have the dedicated ".env" file

3. Check you have docker installed on your system, if not install it from [here](https://docs.docker.com/get-docker/)

4. Next Run
```powershell
./scripts/setup.ps1
```
5. Then Run
```powershell
./scripts/activate-venv.ps1
```
6. To check the django version Run
```powershell
./scripts/check-django.ps1
```
7. Run
```powershell
python manage.py mirgate

python populate_db.py
```
8. And Finally Run
```powershell
./scripts/run-docker.ps1
```

To see the local version of the project:

Find the locally hosted port, this is should be on your docker desktop if ran correctly.

Commonly - http://localhost:1337

It is possible to automate the deployment process from our implementation of docker (docker compose) from this repository.
