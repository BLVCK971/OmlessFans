# OmlessFans
OnlyFans like for Homeless support with videos as ROI for donators.

# Modules:
## common :
fastapi
- [pytest](https://docs.pytest.org/en/stable/) : easy to write small, readable tests
- [coverage](https://coverage.readthedocs.io/en/7.6.0/): measuring code coverage
json
logging
typing
datetime
pytest-asyncio
asyncio
uvicorn

# How to setup :
create new environnement if none : 
```bash
python -m venv .venv 
```

Then you can start : 
```bash
.venv\Scripts\activate
```

```bash
python -m pip install -r requirements/base.txt
```
```bash
python -m pip install -r requirements/dev.txt
```

and to quit : 
```bash
deactivate
```
# How to test :
```bash
python -m pytest
```
exemple : 
```bash
c:\Users\ypepin\AppData\Local\Programs\Python\Python312\python.exe -m pytest -s
```

# How to start :
Dev :
```bash
uvicorn omless.main:app --reload
```
With logs :
```bash
uvicorn omless.main:app --reload --log-config logging.ini
```

Prod :
```bash
uvicorn omless.main:app --log-config logging.ini
```


# EC2 AWS Deployment :
- prepare a temporary Azure DevOps git Credentials, Then : 

```bash
export RUN_MODE="PROD"
cd ~
mkdir ENV
mkdir ENV/OMLESS
mkdir DATA
mkdir DATA/OMLESS
sudo apt-get install git python3.11-venv
git clone https://Ayming@dev.azure.com/Ayming/Robots%20scraping/_git/robot_atmp/
```
- Enter the temporary password generated

```bash
cd robot_atmp
cp -r ENV.EXAMPLE/. ~/ENV/
ls -ld ~/ENV/OMLESS/.?*
cp -r DATA.EXAMPLE/ ~/DATA
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements/base.txt
python -m pip install -r requirements/prod.txt
python -m uvicorn omless.main:app --reload
```