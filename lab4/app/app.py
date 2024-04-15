from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from functools import wraps
from mysqldb import DBConnector
import mysql.connector as connector

app = Flask(__name__)
application = app
app.config.from_pyfile('config.py')

db_connector = DBConnector(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'
login_manager.login_message = 'Авторизуйтесь для доступа к этому ресурсу'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_id, user_login):
        self.id = user_id
        self.user_login = user_login

def get_roles():
    result = []
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT * FROM roles")
        result = cursor.fetchall()
    return result

@login_manager.user_loader
def load_user(user_id):
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT id, login FROM users WHERE id = %s;", (user_id,))
        user = cursor.fetchone()
    if user is not None:
        return User(user.id, user.login)
    return None

def get_users():
    return [{"user_id": "123", "user_login": "user", "user_password": "1234"}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/secret')
# @check_for_login
@login_required
def secret():
    return render_template('secret.html')

@app.route('/auth', methods = ['POST', 'GET'])
def auth():
    error=''
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me', None) == 'on'
        with db_connector.connect().cursor(named_tuple=True, buffered=True) as cursor:
            print(login)
            cursor.execute("SELECT id, login FROM users WHERE login = %s AND password_hash = SHA2(%s, 256)", (login, password))
            # sql = f"SELECT id, login FROM users WHERE login = '{login}' AND password_hash = SHA2('{password}', 256);"
            # print(sql)
            # cursor.execute(sql)
            print(cursor.statement)
            user = cursor.fetchone()

        if user is not None:
            flash('Авторизация прошла успешно', 'success')
            login_user(User(user.id, user.login), remember=remember_me)
            next_url = request.args.get('next', url_for('index'))
            return redirect(next_url)
        flash('Invalid username or password', 'danger')
    return render_template('auth.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/counter')
def counter():
    session['counter'] = session.get('counter', 0) + 1
    return render_template('counter.html')

@app.route('/users')
def users():
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT users.*, roles.name AS role FROM users LEFT JOIN roles ON users.role_id = roles.id")
        print(cursor.statement)
        users = cursor.fetchall()
    return render_template('users.html', users=users)

@app.route('/users/new', methods = ['POST', 'GET'])
@login_required
def users_new():
    user_data = {}
    if request.method == 'POST':
        fields = ('login', 'password', 'first_name', 'middle_name', 'last_name', 'role_id')
        user_data = {field: request.form[field] or None for field in fields}
        try:
            connection = db_connector.connect()
            with connection.cursor(named_tuple=True) as cursor:
                query = (
                    "INSERT INTO users (login, password_hash, first_name, middle_name, last_name, role_id) VALUES "
                    "(%(login)s, SHA2(%(password)s, 256), %(first_name)s, %(middle_name)s, %(last_name)s, %(role_id)s)"
                )
                cursor.execute(query, user_data)
                print(cursor.statement)
                connection.commit()
            flash('Учетная запись успешно создана', 'success')
            return redirect(url_for('users'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены', 'danger')
    return render_template('users_new.html', user_data=user_data, roles=get_roles())

@app.route('/users/<int:user_id>/edit', methods = ['POST', 'GET'])
@login_required
def users_edit(user_id):
    user_data = {}
    with db_connector.connect().cursor(named_tuple=True, buffered=True) as cursor:
        query = ("SELECT first_name, middle_name, last_name, role_id "
                 "FROM users WHERE id = %s")
        cursor.execute(query, [user_id])
        user_data = cursor.fetchone()
        if user_data is None:
            flash('Пользователя нет в базе данных', 'danger')
            return redirect(url_for('users'))
    if request.method == 'POST':
        pass
    return render_template('users_edit.html', user_data=user_data)

