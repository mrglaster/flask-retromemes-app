from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
import os
import sqlite3 as sl

from modules.dummies import generate_dummypage
# from modules.database import get_table_column, create_connection

app = Flask(__name__, template_folder='templates')

CURRENT_ADDRESS = "http://127.0.0.1:5000/"
UPLOAD_FOLDER = "C:\\Users\\79246\\Desktop\\flask-retromemes-app\\static\\images"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'a03cb5d6aa4399201f230dedcbbb3ed8bec0018d19db9521415b547a'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#The page for meme uploading
@app.route("/uploads",methods=['GET','POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload_meme():
	if 'login' not in session:
		return redirect(url_for('login_user'))
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' in request.files:
			file = request.files['file']
			# if user does not select file, browser also
			# submit an empty part without filename
			if file.filename != '' and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return redirect(url_for('show_feed'))
	return render_template('upload.html')

#The feed page
@app.route("/feed", methods=['GET', 'POST'])
def show_feed():
	return render_template("index.html")

#Handling of 404 error
@app.errorhandler(404)
def page_notexist(e):
	return render_template('404.html')

#Register page
@app.route("/register", methods=['POST', 'GET'])
@app.route("/signup", methods=['POST', 'GET'])
def register_user():
	if 'login' in session:
		return redirect(url_for('show_feed'))
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')
		email = request.form.get('email')
		file = ''
		if 'file' in request.files:
			file = request.files['file']
		path = ''
		if file == '':
			path = "C:\\Users\\79246\\Desktop\\flask-retromemes-app\\static\\images\\ava.jpg"
		elif allowed_file(file.filename):
			filename = secure_filename(file.filename)
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(path)
		con = sl.connect('C:\\Users\\79246\\Desktop\\flask-retromemes-app\\database\\memes.db')
		sql = f"INSERT INTO users(login, password, avatar) values('{login}','{password}', '{path}')"
		con.execute(sql)
		session['login'] = login
	return render_template('register.html')

#Login page
@app.route("/login", methods=['POST', 'GET'])
@app.route("/auth", methods=['POST', 'GET'])
@app.route("/authorize", methods=['POST', 'GET'])
def login_user():
	if 'login' in session:
		del session['login'] # TODO delete that later
		return redirect(url_for('show_feed'))
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')
		con = sl.connect('C:\\Users\\79246\\Desktop\\flask-retromemes-app\\database\\memes.db')
		sql = f"SELECT password,id FROM users WHERE `login`='{login}'"
		result = list(con.execute(sql))
		if password == result[0][0]:
			session['login'] = login
			session['id'] = result[0][1]
	return render_template('auth.html')

#Programm run
if __name__=='__main__':
	app.run(host="0.0.0.0")
