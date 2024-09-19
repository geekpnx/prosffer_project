# **PROSFFER**

These steps below is only when you have cloned the repo.

## **STEP 1**

After, you need to go to  **`prosffer`** folder.

- With the command:

```bash
cd prosffer
```

## **STEP 2**

Create virtual environment with **`venv`**.

- With the command:

```bash
python3 -m venv .venv --prompt prosffer
```

Activate **`venv`**

- With the command:

```bash
source .venv/bin/activate
```

## **STEP 3**

Install requirements.

- With the command:

```bash
make dev-install
```


## **STEP 4**

Create **`.env`** file

- With the command

```bash
nano .env
```
Copy and paste texts below inside the file **`.env`**.

```bash
SECRET_KEY=      
DB_NAME=
DB_USER=
DB_PWD=
DB_PORT=5432
DB_HOST=localhost
```


## **STEP 5**

Your may  want to generate your own `SECRET_KEY`
by running the script in **`generate_SECRET_KEY.py`** file.

- With the command 

```bash
python3 scripts/generate_SECRET_KEY.py
```

or run below command in **`iPython`**

```py
import secrets

secrets.token_urlsafe(50)
```

## **STEP 6**

**Note:** *Before you create the database, please make sure your PostgreSQL are runnning and you able to access postgres database with the username postgres*

Create database for the **`DB_NAME`**, if you haven't create it already in your PostgreSQL. You can name it `prosffer_db` (or something else you desire).

- With the command

```bash
python3 scripts/create_DB_NAME.py
```

or by going to PostgreSQL shell directly

- With the command

```bash
psql -U postgres
```

 and enter the query below

```sql
CREATE DATABASE prosffer_db;
```

## **STEP 7**

We might want to create database user for the **`DB_USER`** with the name `prosffer_user` (or name it as you wish) as super user with password for the **`DB_PWD`** `password123` (same here you can set the password as you like)

- With the command

```bash
python3 scripts/create_DB_USER_n_DB_PWD.py
```

or by type in the below query in **PostgreSQL** shell

```sql
CREATE ROLE prosffer_user WITH LOGIN SUPERUSER 'password123';
```


And add this information into the **`.env`** file.

## **STEP 8**

After **`.env`** file been setup with the required data, you can migrate the django  project `prosffer`.

- With the command

```bash
make dev-m
```

## **STEP 9**

Create superuser with the name **`admin`** (or as you wish) and password **`admin`** (or as you wish), to have access to the administrator Django page

- With the command

```bash
make dev-super
```


## **STEP 10**

To run the django server by running the command below in terminal.

```bash
make
```

Check if your Django server is up and running, by going to your browser, and enter **http://127.0.0.1:8000**