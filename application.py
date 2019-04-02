import datetime

import pymysql

from flask import Flask, render_template, request

from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)


@app.route('/')
def index():
    # Get the current time.
    dt = datetime.datetime.now()
    # Assign the variables, convert to string.
    date = dt.strftime("%Y-%m-%d")
    # Set up events list.
    events = [
        'Mid-term exams',
        'Staff annual party',
        'Added from Python code'
    ]
    # Render the template with arguments.
    return render_template('index.html', date=date, events=events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data == 'admin' and form.password.data == 'admin':
            message = 'Login succeed, taking you to the admin page.'
            return render_template('login.html', message=message)
        else:
            message = 'Login failed.'
            return render_template('login.html', message=message)
    else:
        message = 'Test username: admin, password: admin'
        return render_template('login.html', message=message)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        pass
    else:
        return render_template('query.html', date='Input a date on the right', events=['Input a date on the right'])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


class DatabaseOperations():
    __db_url = '172.16.199.106'
    __db_username = 'billjrzhong'
    __db_password = 'taizuatUIC2018'
    __db = ''

    def __init__(self):
        """Connect to database when the object is created."""
        self.__db = self.db_connect()

    def __del__(self):
        """Disconnect from database when the object is destroyed."""
        self.__db.close()

    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username, self.__db_password)
        return self.__db

    def query_events_by_date(self, date):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        date_str = date.strftime('%Y-%m-%d')
        try:
            cursor.execute(
                'SELECT * FROM `events` WHERE `events.event_id` = (SELECT `event_id` FROM `dates` INNER JOIN `dates_events` WHERE `dates.date` = %s)',
                date_str)
            results = cursor.fetchall()
            return results
        except:
            return None

    def add_events_by_date(self, date, events):
        pass

    def delete_events_by_date(self, date, event_id):
        pass
