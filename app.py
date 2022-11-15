from flask import Flask, render_template
from flask import flash, request, redirect, url_for
import random, os

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
