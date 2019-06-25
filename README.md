# UIC-Calendar
A simple demo Flask project for Software Development Workshop II, BNU-HKBU United International College.

## Features

- Get current date from the server computer.
- List events for a given date.

## How to use

- Prepare your Python environment and a MySQL server.
- Import the database schema from the file `database-schema.sql`.
- Add your MySQL information to line 112-115 at `application.py`.
- Install the packages below by `pip`,
  - flask
  - pymysql
  - flask_login
  - wtforms
- Set environment variables and run Flask development server (more detail at [here](http://flask.pocoo.org/)).
