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


app = Flask(__name__, template_folder='templates')

CURRENT_ADDRESS = "http://127.0.0.1:5000/"
DATABASE_PATH = os.getcwd() + '\\' + "database" + '\\' + "memes.db"
UPLOAD_FOLDER = os.getcwd() + '\\' + "static\\images\\uploaded_memes\\"
DEFAULT_AVATAR = os.getcwd() + "\\static\\images\\ava.png"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
				filename = str(date.today())+"_time_"+str(time.time())+".png"
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				connection = create_connection(DATABASE_PATH)
				add_data(connection=connection, tablename='post', dataclass_element=Post(id=0, author_id=get_userid_byname(username, DATABASE_PATH), text=request.form.get('comment'), image=filename, date=str(date.today()), like=0, dislike=0))
				return redirect(url_for('show_feed'))
	return render_template('upload.html')


# The feed page
@app.route('/')
@app.route("/feed", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
def show_feed():
	return render_template("index.html")


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/adminpannel', methods=['GET', 'POST'])
@app.route('/adminpanel', methods=['GET', 'POST'])
def admin_panel():
	try:
		username = session['login']
		connection = create_connection(DATABASE_PATH)
		if is_user_admin(connection, username, 'login'):
			return render_template('admin.html')
		return generate_notadmin_page()
	except:
		return generate_notadmin_page()

# Handling of 404 error
@app.errorhandler(404)
def page_notexist(e):
	return render_template('404.html')


# Register page
@app.route("/register", methods=['POST', 'GET'])
@app.route("/signup", methods=['POST', 'GET'])
def register_user():
	if 'login' in session:
		return redirect(url_for('show_feed'))
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')
		#email = request.form.get('email')
		file = ''
		if 'file' in request.files:
			file = request.files['file']
		path = ''
		if file == '':
			path = DEFAULT_AVATAR
		elif allowed_file(file.filename):
			filename = secure_filename(file.filename)
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(path)
		con = sl.connect(DATABASE_PATH)
		email = f"user_email_{login}{path[len(path)-4:]}@mail.ru"
		val = add_data(connection=con, tablename='users', dataclass_element=User(0, 0, login, password, path, email), individual_fields=USERS_INDIVIDUAL_FIELDS)
		session['login'] = login
	return render_template('register.html')


# Login page
@app.route("/login", methods=['POST', 'GET'])
@app.route("/auth", methods=['POST', 'GET'])
@app.route("/authorize", methods=['POST', 'GET'])
def login_user():
	if 'login' in session:
		del session['login']  # TODO delete that later
		return redirect(url_for('show_feed'))
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')
		con = sl.connect(DATABASE_PATH)
		sql = f"SELECT password,id FROM users WHERE `login`='{login}'"
		result = list(con.execute(sql))
		if password == result[0][0]:
			session['login'] = login
			session['id'] = result[0][1]
	return render_template('auth.html')




# Programm run
if __name__ == '__main__':
	#add_admin(DATABASE_PATH, "billy_herrington")
	app.run(host="0.0.0.0")
