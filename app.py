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
from database.likes import *

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
    if 'login' not in session:
        return redirect(url_for('login_user'))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            username = session['login']
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = str(date.today()) + "_time_" + str(time.time()) + file.filename.rsplit('.', 1)[-1]
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
    if 'login' not in session:
        return redirect(url_for('login_user'))
    if request.method == "POST":
        if 'delete' in request.form.keys():
            id = request.form['id']
            author_id = list(get_authorid_by_post(create_connection(DATABASE_PATH), id))[0][0]
            if session['admin'] >= 1 or session['id'] == author_id:
                delete_post_bID(id, create_connection(DATABASE_PATH), UPLOAD_FOLDER)
                return redirect(url_for('show_feed'))
        if 'like' in request.form.keys():
            id = request.form['id']
            # import_history(id, session['id'], 1)
    if request.method == "GET" and request.args.get('page'):
        page = int(request.args.get('page'))
    dataposts = list(get_all_tabledata(create_connection(DATABASE_PATH), 'Post'))
    pages, limit = calc_pages_and_limit(dataposts, page)
    posts = generate_posts(dataposts, page, limit)
    return render_template("index.html", posts=posts, pages=pages)


def process_useraction(action, nickname):
    if action == 'Delete':
        delete_user(create_connection(DATABASE_PATH), nickname)
    elif action == 'Make admin':
        make_admin(create_connection(DATABASE_PATH), nickname)
    elif action == 'Make moderator':
        make_moderator(create_connection(DATABASE_PATH), nickname)
    elif action == 'Make user':
        make_user(create_connection(DATABASE_PATH), nickname)
    elif action == 'Ban':
        ban_user()
    else:
        return render_template('500.html')

@app.route('/admin', methods=['GET', 'POST'])
@app.route('/adminpannel', methods=['GET', 'POST'])
@app.route('/adminpanel', methods=['GET', 'POST'])
def admin_panel():
    if 'login' not in session:
        return redirect(url_for('login_user'))
    userid = session['id']
    if request.method == "GET" and 'id' in request.args.keys():
        userid = int(request.args['id'])
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
            process_useraction(action, nickname)

    dataposts = list(get_author_posts(create_connection(DATABASE_PATH), userid))
    pages, limit = calc_pages_and_limit(dataposts, page)
    posts = generate_posts(dataposts, page, limit)
    avatar = 'images/avatars/' + get_user_avatar_bId(userid, DATABASE_PATH)
    userdata = {'id': userid, 'login': get_username_bId(userid, DATABASE_PATH),
                'admin': int(list(get_admin_status_bId(userid, DATABASE_PATH))[0][0])}
    return render_template('admin.html', posts=posts, pages=pages, avatar=avatar, userdata=userdata)

def log_out():
    keys = list(session.keys())[:]
    for key in keys:
        session.pop(key)

def generate_posts(dataposts, page, limit):
    posts = []
    # Generate posts
    for i in range((page - 1) * PAGES_POSTS, limit):
        author_name = get_username_bId(dataposts[i][1], DATABASE_PATH)
        avatar = get_user_avatar_bId(dataposts[i][1], DATABASE_PATH)
        reactions = list(get_reaction_bId(dataposts[i][0], DATABASE_PATH))
        post = {'id': dataposts[i][0], 'avatar': AVATAR_FOLDER + avatar, 'author_id': dataposts[i][1],
                'author_name': author_name, 'date': dataposts[i][4], 'comment': dataposts[i][2],
                'image': MEMES_FOLDER + dataposts[i][3], 'likes': reactions[0][0], 'dislikes': reactions[0][1]
                }
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


@app.errorhandler(404)
def page_notexist(e):
    return render_template('404.html')

@app.errorhandler(403)
def page_access_denied(e):
    return render_template('403.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html')



# Register page
@app.route("/register", methods=['POST', 'GET'])
@app.route("/signup", methods=['POST', 'GET'])
def register_user():
    if 'login' in session:
        return render_template("welcome_page.html")
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        # email = request.form['email']
        file = ''
        if 'avatar' in request.files:
            file = request.files['avatar']
        filename = 'ava.jpg'
        path = ''
        if file == '':
            path = DEFAULT_AVATAR
        elif allowed_file(file.filename):
            filename = secure_filename(login + '_' + file.filename)
            path = os.path.join(app.config['UPLOAD_AVATAR_FOLDER'], filename)
            file.save(path)
        con = sl.connect(DATABASE_PATH)
        email = f"user_email_{login}{path[len(path) - 4:]}@mail.ru"
        print(filename)
        val = add_data(connection=con, tablename='users', dataclass_element=User(0, 0, login, password, filename, email),
                       individual_fields=USERS_INDIVIDUAL_FIELDS)
        if val == 100:
            return render_template('cant_register.html')
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
        return render_template('welcome_page.html')
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        con = sl.connect(DATABASE_PATH)
        sql = f"SELECT password,id, admin FROM users WHERE `login`='{login}'"
        result = list(con.execute(sql))
        if len(result) == 0 or password != result[0][0]:
            return render_template("cant_login.html")
        if password == result[0][0]:
            session['login'] = login
            session['id'] = result[0][1]
            session['admin'] = result[0][2]
        return render_template("welcome_page.html")
    return render_template('auth.html')


# Programm run
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
