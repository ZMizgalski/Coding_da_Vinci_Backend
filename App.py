import io

from flask import Flask, Response, request, flash, send_file, jsonify, make_response, render_template, redirect
from flask_cors import cross_origin

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route('/renderImage', methods=["POST"])
@cross_origin()
def hello_world():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        return send_file(io.BytesIO(file.stream.read()), mimetype="image/jpeg")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.run(port=8080, debug=False)
