import base64
import datetime
from functools import wraps

from flask import Flask, render_template

from mysqldb import DBConnector

app = Flask(__name__)
application = app
app.config.from_pyfile('config.py')

db_connector = DBConnector(app)


def b64encode(data):
    if data:
        return base64.b64encode(data).decode('utf-8')


app.jinja_env.filters['b64encode'] = b64encode


def db_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time, end_time = None, None
        connection = db_connector.connect()
        try:
            start_time = datetime.datetime.now()
            with connection.cursor(named_tuple=True, buffered=True) as cursor:
                result = func(cursor, *args, **kwargs)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            end_time = datetime.datetime.now()
            print(f"Duration {func}: {end_time - start_time}")
            # connection.close()
        return result

    return wrapper


from auto import bp as auto_bp, init_login_manager

app.register_blueprint(auto_bp)
init_login_manager(app)


from books import bp as books_bp

app.register_blueprint(books_bp)


@app.route('/')
def index():
    return render_template('index.html')
