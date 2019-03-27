import datetime

from flask import Flask, render_template

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

@app.route('/login')
def login():
    message = 'Test message'
    return render_template('login.html', message=message)