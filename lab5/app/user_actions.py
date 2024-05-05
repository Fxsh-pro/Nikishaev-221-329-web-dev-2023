import csv
from io import BytesIO
from flask import Blueprint, render_template, request, send_file
from app import db_connector, db_operation
from math import ceil

# create table user_actions (
#     id int primary key auto_increment,
#     user_id int,
#     path varchar(100) not null,
#     created_at timestamp default current_timestamp,
#     foreign key (user_id) references users(id)
# ) engine innodb

bp = Blueprint('user_actions', __name__, url_prefix='/user_actions')
MAX_PER_PAGE = 10


@bp.route('/')
@db_operation
def index(cursor):
    page = request.args.get('page', 1, type=int)
    query = ("SELECT last_name, first_name, middle_name, "
             "path, user_actions.created_at AS created_at "
             "FROM user_actions LEFT JOIN users ON user_actions.user_id = users.id "
             f"LIMIT {MAX_PER_PAGE} OFFSET {(page - 1) * MAX_PER_PAGE}")
    cursor.execute(query)
    user_actions = cursor.fetchall()

    query = "SELECT COUNT(*) as count FROM user_actions"
    cursor.execute(query)
    record_count = cursor.fetchone().count
    page_count = ceil(record_count / MAX_PER_PAGE)
    pages = range(max(1, page - 3), min(page_count, page + 3) + 1)

    return render_template("user_actions/index.html", user_actions=user_actions,
                           page=page, pages=pages, page_count=page_count)


@bp.route('users_stats')
@db_operation
def users_stats(cursor):
    query = ("SELECT user_id, last_name, first_name, middle_name, "
             "COUNT(*) AS entries_counter "
             "FROM user_actions LEFT JOIN users ON user_actions.user_id = users.id "
             "GROUP BY user_id ")
    cursor.execute(query)
    users_stats = cursor.fetchall()

    return render_template("user_actions/users_stats.html", users_stats=users_stats)


@bp.route('user_export.csv')
@db_operation
def user_export(cursor):
    query = ("SELECT user_id, last_name, first_name, middle_name, "
             "COUNT(*) AS entries_counter "
             "FROM user_actions LEFT JOIN users ON user_actions.user_id = users.id "
             "GROUP BY user_id ")
    cursor.execute(query)
    print(cursor.statement)
    users_stats = cursor.fetchall()
    result = ''
    fields = ['last_name', 'first_name', 'middle_name', 'entries_counter']
    none_values = ['не', 'авторизованный', 'пользователь']
    result += ','.join(fields) + '\n'
    for record in users_stats:
        if record.user_id is None:
            result += ','.join(none_values) + ',' + str(record.entries_counter) + '\n'
            continue
        result += ','.join([str(getattr(record, field)) for field in fields]) + '\n'

    return send_file(BytesIO(result.encode()), as_attachment=True, mimetype='text/csv', download_name='user_export.csv')


@bp.route('paths_stats')
def paths_stats():
    # with db_connector.connect().cursor(named_tuple=True) as cursor:
    #     query = ("select last_name, first_name, middle_name, "
    #              "path, user_actions.created_at as created_at "
    #              "from user_actions left join users on user_actions.user_id = users.id")
    #     cursor.execute(query)
    #     user_actions = cursor.fetchall()
    return render_template("user_actions/paths_stats.html")
