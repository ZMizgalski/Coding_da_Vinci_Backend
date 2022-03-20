import io

from flask import Flask, Response, request, flash, send_file, jsonify, make_response, render_template, redirect
from flask_cors import cross_origin
from picture_mixer import InitializeMixer
from picture_mixer.servieces import DataHolder

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route('/getData', methods=["GET"])
@cross_origin()
def getData():
    with open('picture_mixer/servieces/data.json', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype="application/json")


# @app.route('/renderImage', methods=["POST"])
# @cross_origin()
# def hello_world():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         images = []
#         for file in request.files:
#             images.append(file)
#         InitializeMixer.InitializeMixer(images)
#         image = DataHolder.images[0]
#         DataHolder.images.clear()
#
#         return send_file(io.BytesIO(image.stream.read()), mimetype="image/jpeg")
#
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#

app.run(port=8080, debug=False)
