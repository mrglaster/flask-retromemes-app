from flask import Flask
from flask import redirect
from flask import render_template
from os import getcwd

app = Flask(__name__, template_folder='templates')

CURRENT_ADDRESS = "http://127.0.0.1:5000/"


#The page for meme uploading
@app.route("/uploads",methods=['GET','POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload_meme():
	return render_template('upload.html')

#The feed page
@app.route("/feed", methods=['GET', 'POST'])
def show_feed():
	return "<h1>Welcome to da feed page!</h1>"

#Handling of 404 error
@app.errorhandler(404)
def page_notexist(e):
	return render_template('404.html')

#Register page
@app.route("/register", methods=['POST', 'GET'])
def register_user():
	return "<h2>Welcome to register page!</h2>"

#Login page
@app.route("/login", methods=['POST', 'GET'])
@app.route("/auth", methods=['POST', 'GET'])
@app.route("/authorize", methods=['POST', 'GET'])
def login_user():
	return "<h2> Welcome to the  login page </h2>"

#Programm run
if __name__=='__main__':
	app.run(host="0.0.0.0")
