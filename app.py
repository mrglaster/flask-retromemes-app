from flask import Flask, render_template
from flask import flash, request, redirect, url_for
import random, os

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "<p>Hello world!</p>"

app.config['UPLOAD_FOLDER'] = 'C:/'
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    print(request)
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
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html', )


if __name__=='__main__':
	app.run(host="0.0.0.0")
