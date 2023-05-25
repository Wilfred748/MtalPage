from flask import *
import sqlite3
from flask_login import login_user, LoginManager, login_required, logout_user, current_user, AnonymousUserMixin, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash 
from wtforms.validators import DataRequired, EqualTo, Length
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from myapp.decorators import any_administrator_required
from werkzeug.security import check_password_hash

from config import config

from models.ModelUser import ModelUser

from User import AnonymousUser


# Entities:
#from models.entities.User import User

#USUARIO: ADMINISTRADOR_BD_WIL
#CONTRASENNA: r4-BjvW6g0Aar4L-orvrtSVWlaxWLhgm

app = Flask(__name__, template_folder='templatesFile', static_folder='staticsFile')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'
DATABASE = 'productos_tkp.db'

db = MySQL(app)
csrf = CSRFProtect()

app.secret_key = "r4-BjvW6g0Aar4L-orvrtSVWlaxWLhgm"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///productos_tkp.db" 

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.before_first_request
def crear_products_db():
    connect = sqlite3.connect('productos_tkp.db')
    cursor = connect.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos_tkp'")

    if cursor.fetchone():
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos_tkp'")
    else:
        cursor.execute("CREATE TABLE productos_tkp(ID integer, name text, description text, categoria text ,img_url text, price integer)")
    connect.commit()


def connect_product_db():
    return sqlite3.connect('productos_tkp.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.route("/", methods=['GET', 'POST'])
def main():
    #print(generate_password_hash("r4-BjvW6g0Aar4L-orvrtSVWlaxWLhgm"))
    busqueda()
    return render_template('main.html')

@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

@app.route("/tienda")
def tienda():
    busqueda()
    con = connect_product_db()
    cur = con.cursor()

    statement = f"SELECT name, description, price, img_url from productos_tkp"

    result = cur.execute(statement)
    results = result.fetchall()

    names = [r[0] for r in results]
    descriptions = [r[1] for r in results]
    prices = [r[2] for r in results]
    img_urls = [r[3] for r in results]


    db = get_db()
    cursor = db.cursor()
    category = request.args.getlist('category')
    price = request.args.get('price', default=0, type=int)
    query = 'SELECT * FROM productos_tkp'
    params = []
    if category and price:
        query += ' WHERE ' + ' AND '.join(['categoria=?'] * len(category)) + ' AND price<=?'
        params = category + [price]
    elif category:
        query += ' WHERE ' + ' OR '.join(['categoria=?'] * len(category))
        params = category
    elif price:
        query += ' WHERE price<=?'
        params = [price]
    cursor.execute(query, params)
    products = cursor.fetchall()
    categories = set([p['categoria'] for p in products])

    return render_template("tienda.html",
        names=names, 
        descriptions=descriptions,
        prices=prices, 
        img_urls=img_urls, 
        products=products, 
        categories=categories, 
        selected_categories=category, 
        selected_price=price
        )

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phonenumber = request.form['phonenumber']
        gender = request.form["gender"]

        hashed_pw = generate_password_hash(password, "sha256")

        #con = mysql.connect() #connect_db()
        cur = db.connection.cursor()

        cur.execute("INSERT into usuarios(name, email, password, phonenumber, gender) VALUES(%s,%s,%s,%s,%s)", (name, email, hashed_pw, phonenumber, gender))
        db.connection.commit()
        cur.close()

        return render_template('loginform.html')

    return render_template('registrationform.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        if AnonymousUserMixin.is_active:
            id = -1
            email = "anonimo@gmail.com"
            name="guest"
            role = "user"

        usuarios = User(0, request.form["email"], request.form["password"], role)

        logged_user = ModelUser.login(db, usuarios)

        if logged_user != None:
                
            if check_password_hash(logged_user.password, usuarios.password):
                login_user(logged_user)

                if current_user.email == 'wilfredoperalta293@outlook.com':
                    session['logged_in'] = True
                    current_user.role = 'admin' 
                    session['role'] = 'admin' # Assign "admin" role to the user
                    return redirect(url_for('admin'))
                
                return redirect(url_for('main'),)
            
            else:
                flash("Invalid password...")
                return render_template('loginform.html')
        else:
            flash("mail not found...")
            return render_template('loginform.html')
    else:
        return render_template("loginform.html")

@app.route("/terminos y condiciones")
def terms():
    return render_template("termsANDconditions.html")

@app.route("/favitems")
@login_required
def favitems():
    return render_template('fav_items.html')

@app.route("/your account")
@login_required
def account_info():
    logout()
    busqueda()
    return render_template('account_info.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User has logout...")
    return redirect(url_for('login'))


@app.route("/admin", methods = ['GET', 'POST'])
#@any_administrator_required
def admin():

    if AnonymousUser.is_active:
        id = -1

    if current_user.id == 1:
        session['role'] = 'admin'
    # logged_user.email == 'wilfredoperalta293@outlook.com' or
        flash("Welcome Patrón!!!")
        if request.method == 'POST':
            name = request.form["name"]
            description = request.form["description"]
            price = request.form["price"]
            categoria = request.form["categoria"]
            img_url = request.form["img_url"]

            con = connect_product_db()
            cur = con.cursor()

            cur.execute("INSERT into productos_tkp(name, description, price, categoria, img_url) VALUES(?,?,?,?,?)", (name, description, price, categoria, img_url))
            print(name, description, price, categoria, img_url)
            con.commit()
            con.close()
            return render_template("crear_producto.html")
        return render_template("crear_producto.html")
    else:
        flash("Vo' no so' admin")
        return redirect(url_for('main'))
    
    

    
@app.route('/busqueda', methods=["POST", "GET"])
def busqueda():
    
    if request.method == 'POST':
        name = request.form["name"]

        con = connect_product_db()
        cur = con.cursor()
        

        statement = f"SELECT name, description, price, img_url from productos_tkp WHERE name LIKE '%{name}%'"

        result = cur.execute(statement)
        results = result.fetchall()

        names = [r[0] for r in results]
        descriptions = [r[1] for r in results]
        prices = [r[2] for r in results]
        img_urls = [r[3] for r in results]

        return render_template("busqueda.html",
            names=names, 
            descriptions=descriptions,
            prices=prices, 
            img_urls=img_urls,
            )
    
    elif request.method == "GET":
        name = request.args.get("name")

        con = connect_product_db()
        cur = con.cursor()
        

        statement = f"SELECT name, description, price, img_url from productos_tkp WHERE name LIKE '%{name}%'"

        result = cur.execute(statement)
        results = result.fetchall()

        names = [r[0] for r in results]
        descriptions = [r[1] for r in results]
        prices = [r[2] for r in results]
        img_urls = [r[3] for r in results]

        return render_template ("busqueda.html",
            names=names, 
            descriptions=descriptions,
            prices=prices, 
            img_urls=img_urls)
        
    return render_template("busqueda.html")

@app.route("/cart")
@login_required
def cart():
    return ("cart.html")

def status_401(error):
    flash("You should be logged to go there")
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

def status_403(error):
    return redirect(url_for('main')), 403

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.register_error_handler(403, status_403)
    app.run()                                                                                                             

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

class User(UserMixin):

    def __init__(self, id, email, password, role, name="", ) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

class AnonymousUser(AnonymousUserMixin):
    id = -1
    email = "anonimo@gmail.com"
    name="guest"
    role = "user"





