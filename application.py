import datetime

import pymysql

from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user

from wtforms import Form, StringField, PasswordField, DateField, validators

app = Flask(__name__)
app.secret_key = b'UIC-Calendar-20190408'

login_manager = LoginManager()
login_manager.init_app(app)


class CalendarAdmin(UserMixin):
    """User class for flask-login"""

    def __init__(self, id):
        self.id = id
        self.name = 'admin'
        self.password = 'admin'
        # self.is_authenticated = True
        # self.is_active = True
        # self.is_anonymous = False


@login_manager.user_loader
def load_user(user_id):
    return CalendarAdmin(user_id)


@app.route('/')
def index():
    # Get the current time.
    dt = datetime.datetime.now()
    # Assign the variables, convert to string.
    date = dt.strftime("%Y-%m-%d")
    db_op = DatabaseOperations()
    result = db_op.query_events_by_date(date)
    if result is None or len(result) is 0:
        result = ['No event']
    else:
        pass
    return render_template('index.html', date=date, events=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data == 'admin' and form.password.data == 'admin':
            test_admin_user = CalendarAdmin('admin')
            login_user(test_admin_user)
            return redirect('./admin')
        else:
            message = 'Login failed.'
            return render_template('login.html', message=message)
    else:
        message = 'Test username: admin, password: admin'
        return render_template('login.html', message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('.')


@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryDateForm(request.form)
    if request.method == 'POST' and form.validate():
        db_op = DatabaseOperations()
        result = db_op.query_events_by_date(form.date.data)
        if result is None or len(result) is 0:
            result = ['No event']
        else:
            pass
        return render_template('query.html', date=form.date.data, events=result)
    else:
        return render_template('query.html', date='Input a date on the right', events=['Input a date on the right'])


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


class QueryDateForm(Form):
    date = DateField('date')


class DatabaseOperations():
    __db_url = '172.16.199.106'
    __db_username = 'billjrzhong'
    __db_password = 'taizuatUIC2018'
    __db_name = 'billjrzhong'
    __db = ''

    def __init__(self):
        """Connect to database when the object is created."""
        self.__db = self.db_connect()

    def __del__(self):
        """Disconnect from database when the object is destroyed."""
        self.__db.close()

    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username, self.__db_password, self.__db_name)
        return self.__db

    def query_events_by_date(self, date):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = 'SELECT event FROM `events` WHERE `event_id` = ' \
                  '(SELECT `event_id` FROM `dates` INNER JOIN `dates_events` ON dates.date_id = dates_events.date_id ' \
                  'WHERE `date` = str_to_date("{0}","%Y-%m-%d"))'.format(str(date))
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def add_events_by_date(self, date, events):
        pass

    def delete_events_by_date(self, date, event_id):
        pass
