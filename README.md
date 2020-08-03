# Traceable - Python Django - Merchant MicroServices
This repository has all the API related to Merchant microservices.

Minimal [Django](https://simpleisbetterthancomplex.com/article/2017/08/07/a-minimal-django-application.html) sample app.

## Requirements
- [Python3](https://www.python.org/download/releases/3.0/)
- [Postgres DB](https://www.postgresql.org/download/linux/ubuntu/)
- [Traceable - Spring Boot - User microservices application](https://git.hashedin.com/nawaz.alam/traceable-user-microservices)

## Steps for Local Setup:

- On the command line
- Clone the repo
```commandline
git clone git@git.hashedin.com:nishanth.p/traceable-merchant.git
```
- cd to the project root directory
```commandline
cd traceable-merchant
```
- Create a virtual environment for the application(generally named venv).
```commandline
python3 -m venv <venv-name>
```
- Activate this virtualenv whenever using this application.
```commandline
source <venv-name>/bin/activate
```
- Upgrade pip
```commandline
python3 -m pip install --upgrade pip
```
- Install all the dependencies listed in requirements.txt
```commandline
pip install -r requirements.txt
```
<!--
- Add `.env` inside the root directory of the application.

##### Directory Structure
```
traceable-merchant
├── traceable
│   └── 
├── traceable_site
│   └── 
├── user
│   └── 
├── <venv-name>
├── manage.py
└── .env
```
- Add contents for `.env` file
-->
- Export the following environment variables
- Make sure you give the same database name provided for [Traceable - Spring Boot - User microservices application](https://git.hashedin.com/nawaz.alam/traceable-user-microservices)
- Make sure all the permissions on the database is granted for the database-user.
- Make sure you give the same `JWT_SECRET` provided for [Traceable - Spring Boot - User microservices application](https://git.hashedin.com/nawaz.alam/traceable-user-microservices)

```.env
export DB_NAME=<database-name>
export DB_USER=<db-username>
export DB_PASSWORD=<db-user-password>
export DB_HOST=<db-url-host>
export DB_PORT=<db-url-port>
export JWT_SECRET=<jwt-secret-key>
export GOOGLE_APPLICATION_CREDENTIALS=<path-to-gcp-key-file.json>
export GCP_BUCKET_NAME=<GCP-bucket-name>
```
- Perform fake migrations on `user` app as tables related to users are created by [Traceable - Spring Boot - User microservices application](https://git.hashedin.com/nawaz.alam/traceable-user-microservices)
```commandline
python manage.py makemigrations user
python manage.py migrate user --fake
```
- Perform migrations on traceable app. New tables required will be created now.
```commandline
python manage.py makemigrations traceable
python manage.py migrate traceable
```
- Migrations should be performed whenever there are changes in the database schema.

## Running the application locally
```commandline
python3 manage.py runserver
```
- The server starts running.