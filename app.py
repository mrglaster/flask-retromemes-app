import os
import sqlite3 as sl
import sys
import time
from datetime import date
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
from modules.dummies import generate_dummypage
from modules.database import *
from modules.dummies import *
from modules.constants import *

app = Flask(__name__, template_folder='templates')
CURRENT_ADDRESS = "http://127.0.0.1:5000/"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_AVATAR_FOLDER'] = UPLOAD_AVATAR_FOLDER
app.config['SECRET_KEY'] = 'a03cb5d6aa4399201f230dedcbbb3ed8bec0018d19db9521415b547a'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# The page for meme uploading
@app.route("/uploads", methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload_meme():
    check_login()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            username = session['login']
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = str(date.today()) + "_time_" + str(time.time()) + file.filename.split[-1]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                connection = create_connection(DATABASE_PATH)
                add_data(connection=connection, tablename='post',
                         dataclass_element=Post(id=0, author_id=get_userid_byname(username, DATABASE_PATH),
                                                text=request.form.get('comment'), image=filename,
                                                date=str(date.today()), like=0, dislike=0))
        return redirect(url_for('show_feed'))
    return render_template('upload.html')


# The feed page
@app.route('/')
@app.route("/feed", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
def show_feed(page=1):
    check_login()
    if request.method == "GET" and request.args.get('page'):
        page = int(request.args.get('page'))
    dataposts = list(get_all_tabledata(create_connection(DATABASE_PATH), 'Post'))
    pages, limit = calc_pages_and_limit(dataposts, page)
    posts = generate_posts(dataposts, page, limit)
    return render_template("index.html", posts=posts, pages=pages)


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/adminpannel', methods=['GET', 'POST'])
@app.route('/adminpanel', methods=['GET', 'POST'])
def admin_panel():
    check_login()
    page = 1
    if request.method == "GET" and request.args.get('page'):
        page = int(request.args.get('page'))
    if request.method == 'POST':
        if 'exit' in request.form.keys():
            log_out()
            return redirect(url_for('login_user'))
        else:
            action = request.form['action']
            nickname = request.form['nickname']
            match action:
                # case "Ban":
                    # ban_user()
                case "Delete":
                    delete_user(create_connection(DATABASE_PATH), nickname)
                # case "Unban":
                    # unban_user()
                case "Make admin":
                    make_admin(create_connection(DATABASE_PATH), nickname)
                case "Make moderator":
                    make_moderator(create_connection(DATABASE_PATH), nickname)
                case "Make user":
                    make_user(create_connection(DATABASE_PATH), nickname)
    dataposts = list(get_author_posts(create_connection(DATABASE_PATH), session['id']))
    pages, limit = calc_pages_and_limit(dataposts, page)
    posts = generate_posts(dataposts, page, limit)
    avatar = 'images/avatars/' + get_user_avatar_bId(session['id'], DATABASE_PATH)
    return render_template('admin.html', posts=posts, pages=pages, avatar=avatar)

def check_login():
    if 'login' not in session:
        return redirect(url_for('login_user'))

def log_out():
    keys = list(session.keys())[:]
    for key in keys:
        session.pop(key)

def generate_posts(dataposts, page, limit):
    posts = []
    # Generate posts
    for i in range((page - 1) * PAGES_POSTS, limit):
        author_name = get_username_bId(dataposts[i][1], 'C:\\Users\\79246\\PycharmProjects\\flask-retromemes-app\\'
                                                        'database\\memes_testdata.db')
        avatar = get_user_avatar_bId(dataposts[i][1], 'C:\\Users\\79246\\PycharmProjects\\flask-retromemes-app\\'
                                                      'database\\memes_testdata.db')
        post = {'avatar': AVATAR_FOLDER + avatar, 'author_id': dataposts[i][1],
                'author_name': author_name, 'date': dataposts[i][4], 'comment': dataposts[i][2],
                'image': MEMES_FOLDER + dataposts[i][3], }
        posts.append(post)
    return posts

def calc_pages_and_limit(dataposts, page):
    pages = len(dataposts) // PAGES_POSTS
    if len(dataposts) % PAGES_POSTS != 0:
        pages += 1
    limit = page * PAGES_POSTS
    if limit > len(dataposts):
        limit = len(dataposts)
    return pages, limit

# Handling of 404 error
@app.errorhandler(404)
def page_notexist(e):
    return render_template('404.html')


# Register page
@app.route("/register", methods=['POST', 'GET'])
@app.route("/signup", methods=['POST', 'GET'])
def register_user():
    log_out()
    if 'login' in session:
        return redirect(url_for('show_feed'))
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        # email = request.form['email']
        file = ''
        if 'avatar' in request.files:
            file = request.files['avatar']
        path = ''
        if file == '':
            path = DEFAULT_AVATAR
        elif allowed_file(file.filename):
            filename = secure_filename(login + '_' + file.filename)
            path = os.path.join(app.config['UPLOAD_AVATAR_FOLDER'], filename)
            file.save(path)
        con = sl.connect(DATABASE_PATH)
        email = f"user_email_{login}{path[len(path) - 4:]}@mail.ru"
        val = add_data(connection=con, tablename='users', dataclass_element=User(0, 0, login, password, filename, email),
                       individual_fields=USERS_INDIVIDUAL_FIELDS)
        res = list(con.execute(f"SELECT id,admin FROM Users WHERE login='{login}'"))[0]
        session['id'] = res[0]
        session['login'] = login
        session['admin'] = res[1]
        return redirect(url_for('show_feed'))
    return render_template('register.html')


# Login page
@app.route("/login", methods=['POST', 'GET'])
@app.route("/auth", methods=['POST', 'GET'])
@app.route("/authorize", methods=['POST', 'GET'])
def login_user():
    if 'login' in session:
        return redirect(url_for('show_feed'))
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        con = sl.connect(DATABASE_PATH)
        sql = f"SELECT password,id, admin FROM users WHERE `login`='{login}'"
        result = list(con.execute(sql))
        if password == result[0][0]:
            session['login'] = login
            session['id'] = result[0][1]
            session['admin'] = result[0][2]
        redirect('show_feed')
    return render_template('auth.html')


# Programm run
if __name__ == '__main__':
    #create_testdata_database(DATABASE_PATH, "C:\\Users\\Glaster\\Desktop\\memes\\")
    app.run(host="0.0.0.0", debug=True)
