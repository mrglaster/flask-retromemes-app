from flask import Flask
from flask import redirect

app = Flask(__name__)

CURRENT_ADDRESS = "http://127.0.0.1:5000/"


#The page for meme uploading
@app.route("/uploads",methods=['GET','POST'])
def upload_meme():
	return "<h> Welcome to meme uploads page! There is nothing here yet, but soon it will be a cool webpage where you'll can upload new memes! </h>"

#The feed page
@app.route("/feed", methods=['GET', 'POST'])
def show_feed():
	return "<h1>Welcome to da feed page!</h1>"

#Handling of 404 error
@app.errorhandler(404)
def page_notexist(e):
	return "<h1>Yo nigga, diz page doznt exitst, go to da feed page or ozer crap, hier ya won't find anysing</h1>"

#Register page
@app.route("/register", methods=['POST', 'GET'])
@app.route("/newuser", methods=['POST', 'GET'])
def register_user():
	return "<h2>Welcome to register page!</h2>"

#Login page
@app.route("/login", methods=['POST', 'GET'])
@app.route("/auth", methods=['POST', 'GET'])
@app.route("/authorize", methods=['POST', 'GET'])
def login_user():
	return "<h1> Welcome to authorisation page!</h1>"

#Programm run
if __name__=='__main__':
	app.run(host="0.0.0.0")
