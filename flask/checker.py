from functools import wraps
from flask import request
from config import TOKEN


class AuthTokenRequired:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != TOKEN:
            return 'Unauthorized!', 401
        return self.func(*args, **kwargs)
