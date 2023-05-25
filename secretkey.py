import secrets
from flask import *
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(1000)

print(app.secret_key)

password = generate_password_hash("123456789")

print(password)
