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

Go to https://localhost:8000
