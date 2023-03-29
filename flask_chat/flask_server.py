"""File with flask routes."""

from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import DBHandler
from config import INCORRECT, NO_SUCH_USERNAME, MISMATCH, USERNAME_TAKEN


app = Flask(__name__)


@app.route('/')
def index():
    """This method route main page.

    Returns:
        html: html page
    """
    if 'username' in session:
        return render_template('chat.html', messages=get_messages())
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Method that routes login users.

    Returns:
        html: html page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if DBHandler.check_user(username):
            if DBHandler.check_password(username, password):
                session['username'] = request.form['username']
                return redirect(url_for('chat'))
            flash(INCORRECT)
            return redirect(url_for('login'))
        flash(NO_SUCH_USERNAME.format(request.form['username']))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """This method routes registration for users.

    Returns:
        html: html page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conf_password = request.form['confirm-password']
        if password != conf_password:
            flash(MISMATCH)
            return redirect(url_for('register'))
        if DBHandler.reg_user(username, password):
            return redirect(url_for('login'))
        flash(USERNAME_TAKEN)
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/logout', methods=['POST'])
def logout():
    """This method routes logout of users.

    Returns:
        html: html page.
    """
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/send_message', methods=['POST'])
def send_message():
    """This method routes send message of user.

    Returns:
        html: html page.
    """
    DBHandler.send_message(session['username'], request.form['message'])
    return redirect(url_for('chat'))


@app.route('/chat')
def chat():
    """This method routes chat where users communicate.

    Returns:
        html: html page.
    """
    if 'username' not in session:
        return redirect('/login')
    messages = get_messages()
    return render_template('chat.html', messages=messages)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    """This method return all messages.

    Returns:
        json: all messages in chat.
    """
    return DBHandler.get_messages()


@app.route('/favicon.ico', methods=['GET'])
def get_last_messages():
    """This method routes latest 50 messages.

    Returns:
        json: 50 latest messages
    """
    return DBHandler.get_last_messages()
