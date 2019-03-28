import datetime

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
        username = form.username
        password = form.password
        if username.data == 'admin' and password.data == 'admin':
            message = 'Login succeed, taking you to the admin page.'
            return render_template('login.html', message=message)
        else:
            message = 'Login failed.'
            return render_template('login.html', message=message)
    else:
        message = 'Test username: admin, password: admin'
        return render_template('login.html', message=message)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])