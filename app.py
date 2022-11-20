from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
import os

from modules.dummies import generate_dummypage

app = Flask(__name__, template_folder='templates')

CURRENT_ADDRESS = "http://127.0.0.1:5000/"
UPLOAD_FOLDER = '/path/to/the/uploads'
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
	if not 'logged' in session:
		return redirect(url_for('login_user'))
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return render_template('upload.html')

#The feed page
@app.route("/feed", methods=['GET', 'POST'])
def show_feed():
	return

#Handling of 404 error
@app.errorhandler(404)
def page_notexist(e):
	return render_template('404.html')

#Register page
@app.route("/register", methods=['POST', 'GET'])
@app.route("/signup", methods=['POST', 'GET'])
def register_user():
	return generate_dummypage("register")

#Login page
@app.route("/login", methods=['POST', 'GET'])
@app.route("/auth", methods=['POST', 'GET'])
@app.route("/authorize", methods=['POST', 'GET'])
def login_user():
<<<<<<< HEAD
	if request.method == 'POST':
		login = request.
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return render_template("auth.html")
=======
	return generate_dummypage("login")
>>>>>>> 78801c826430937c903cc04e3e7cb8a67e326275

#Programm run
if __name__=='__main__':
	app.run(host="0.0.0.0")
