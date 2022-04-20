import os
import json
from flask import Flask, Response, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
import wget
import shutil
import ssl

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = 'E20467A8B2D5F32E451E1125BE47045DE600AA22F97046263869E291C5A49A67DD47C52D990FE0053D25FD659A4E358DE10A8F9756C9066A13B71AE860728B75'
app.config['UPLOAD_FOLDER'] = 'images'

ssl._create_default_https_context = ssl._create_unverified_context
tmpImages = 'tmpImages'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route("/view/<path:path>", methods=["GET"])
def view(path):
    return send_from_directory("images", path)


@app.route("/download/<path:path>", methods=["GET"])
def download(path):
    return send_from_directory("images", path, as_attachment=True)


@app.route('/getFilesNames', methods=["GET"])
def get_all_filenames():
    return Response(json.dumps({'images': os.listdir("./images")}), status=200, mimetype="application/json")


@app.route('/makePublic', methods=["POST"])
def upload_mixed_file():
    if 'file' not in request.files:
        flash('No file part')
        return Response("Key 'file' not found in request!", status=400)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return Response("No files found!", status=400)
    if file and allowed_file(file.filename):
        print(request.files.getlist('file'))
        if len(request.files.getlist('file')) > 1:
            return Response('Too many files', status=400)
        img = request.files.get('file')
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img.filename)))
        return Response('File uploaded', status=200)
    else:
        return Response("No files found!", status=400)


@app.route('/getData', methods=["GET"])
@cross_origin()
def getData():
    with open('picture_mixer/servieces/data.json', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype="application/json")


def downloadImage(URL, Path):
    return wget.download(URL, Path)


def clear_directory(Path):
    for filename in os.listdir(Path):
        file_path = os.path.join(Path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route('/renderImage', methods=["POST"])
@cross_origin()
def renderImage():
    firstImage = request.values.get('firstImage')
    secondImage = request.values.get('secondImage')

    if firstImage is None:
        flash('No file part')
        return Response("Key 'firstImage' not found in request!", status=400)

    if secondImage is None:
        flash('No file part')
        return Response("Key 'secondImage' not found in request!", status=400)

    clear_directory(tmpImages)
    firstExtension = firstImage.split("/")[7].split('.')[1]
    secondExtension = secondImage.split("/")[7].split('.')[1]
    firstFile = '1.' + firstExtension
    secondFile = '2.' + secondExtension
    downloadImage(firstImage, tmpImages + "\\" + firstFile)
    downloadImage(firstImage, tmpImages + "\\" + secondFile)

    return send_from_directory(tmpImages, firstFile, as_attachment=True)
    # file = request.files['file']
    # if file.filename == '':
    #     flash('No selected file')
    #     return Response("No files found!", status=400)
    #
    #
    #
    # if file and allowed_file(file.filename):
    #     images = []
    #     for file in request.files.getlist('file'):
    #         images.append(file)
    #     mixer = InitializeMixer.InitializeMixer(images)
    #     mixedImage = mixer.getImage()
    #     DataHolder.images.clear()
    #     DataHolder.mixedImage.clear()
    #
    #     return Response(genImg(mixedImage), mimetype="multipart/x-mixed-replace; boundary=frame")
    #
    # else:
    #     return Response("No files found!", status=400)


def genImg(mixedImage):
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + mixedImage + b'\r\n\r\n')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.run(port=8080, debug=False)
