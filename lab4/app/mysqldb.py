from flask import current_app, g
import mysql.connector

# create table if not exists roles ( TODO create tables first
#     id int primary key auto_increment,
#     name varchar(100) not null,
#     description text
# ) engine innodb;
#
# create table if not exists users (
#     id int primary key auto_increment,
#     login varchar(100) not null unique,
#     password_hash varchar(64) not null,
#     last_name varchar(64) not null,
#     first_name varchar(64) not null,
#     middle_name varchar(64),
#     created_at timestamp not null default current_timestamp,
#     role_id int,
#     foreign key (role_id) references roles(id)
# ) engine innodb;

class DBConnector:
    def __init__(self, app):
        self.app = app
        self.app.teardown_appcontext(self.disconnect)

    def get_config(self):
        return {
            'user': self.app.config["MYSQL_USER"],
            'password': self.app.config["MYSQL_PASSWORD"],
            'host': self.app.config["MYSQL_HOST"],
            'database': self.app.config["MYSQL_DATABASE"]
        }

    def connect(self):
        if 'db' not in g:
            g.db = mysql.connector.connect(**self.get_config())
        return g.db
    
    def disconnect(self, e=None):
        if 'db' in g:
            g.db.close()
        g.pop('db', None)
        