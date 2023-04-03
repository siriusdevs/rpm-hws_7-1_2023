"""Mian Flask file for run."""
from config import PASSWORD_ERROR, EMAIL_ERROR, LOGIN_ERROR, USERNAME_ERROR, LOGIN_TEMPLATE, \
    INDEX_TEMPLATE, CHAT_TEMPLATE, REG_TEMPLATE, REG_PATH, INDEX_PATH, LOGIN_PATH, CHAT_PATH, \
    LOGOUT_PATH, COLORS, MAX_NAME_LEN
from flask import Flask, render_template, redirect, request, session
from typing import Callable
from db_utils import DbHandler
from random import choice

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret!123'


@app.route(LOGIN_PATH, methods=['POST', 'GET'])
def login() -> Callable:
    """Function manages log in system.

    Returns:
        Callable - method which redirects on other page or renders templates.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_id = DbHandler.get_user_id(username, password)
        if not user_id:
            return render_template(LOGIN_TEMPLATE, error=LOGIN_ERROR)
        session['user_id'] = user_id
        session['password'] = password
        return redirect(CHAT_PATH)
    return redirect(CHAT_PATH) if session.get('user_id') else render_template(LOGIN_TEMPLATE)


@app.route(LOGOUT_PATH, methods=['GET'])
def logout() -> Callable:
    """Function manages log out system.

    Returns:
        Callable - method which redirects on other page.
    """
    session['user_id'] = None
    return redirect(CHAT_PATH) if session.get('user_id') else redirect(INDEX_PATH)


@app.route(INDEX_PATH, methods=['GET'])
def index() -> Callable:
    """Function which is responsible for rendering main page.

    Returns:
        Callable - method which redirects on other page or renders templates.
    """
    if session.get('user_id'):
        return redirect(CHAT_PATH)
    return render_template(INDEX_TEMPLATE)


@app.route(REG_PATH, methods=['GET', 'POST'])
def registration() -> Callable:
    """Function manages registration system.

    Returns:
        Callable - method which redirects on other page or renders templates.
    """
    if request.method == 'POST':
        # print(request.form.to_dict(flat=False))
        # print(request.data)
        # print(request.headers)
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('username')
        # print(password, email, name)
        if not DbHandler.check_name(name) or len(name) > MAX_NAME_LEN:
            return render_template(REG_TEMPLATE, error=USERNAME_ERROR)
        if not DbHandler.check_email(email):
            return render_template(REG_TEMPLATE, error=EMAIL_ERROR)
        if password == request.form.get('copy_password'):
            DbHandler.registrate(name, email, password, choice(COLORS))
            return redirect(LOGIN_PATH)
        return render_template(REG_TEMPLATE, error=PASSWORD_ERROR)
    return redirect(CHAT_PATH) if session.get('user_id') else render_template(REG_TEMPLATE)


@app.route(CHAT_PATH, methods=['POST', 'GET'])
def fill_chat():
    """Function manages chat filling.

    Returns:
        Callable - method which redirects on other page or renders templates.
    """
    user_id = session.get('user_id')
    password = session.get('password')
    if user_id is None:
        return redirect(LOGIN_PATH)
    if request.method == 'POST':
        username = DbHandler.get_username(user_id)
        DbHandler.add_massage(request.form.get('message'), DbHandler.get_user_id(username, password))
        return redirect(CHAT_PATH)
    return render_template(CHAT_TEMPLATE, messages=DbHandler.fill_page())
