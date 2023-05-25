from functools import wraps
from flask import abort, session

def any_administrator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = session.get('role')
        if role != 'admin':
            #print(role)
            abort(403)
            
        return f(*args, **kwargs)
    return decorated_function


