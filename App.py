from flask import Flask, Response, request, flash, redirect
from flask_cors import cross_origin
from picture_mixer import InitializeMixer
from picture_mixer.servieces import DataHolder

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = 'E20467A8B2D5F32E451E1125BE47045DE600AA22F97046263869E291C5A49A67DD47C52D990FE0053D25FD659A4E358DE10A8F9756C9066A13B71AE860728B75'


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


@app.route('/renderImage', methods=["POST"])
@cross_origin()
def renderImage():
    if 'file' not in request.files:
        flash('No file part')
        return Response("Key 'file' not found in request!", status=400)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return Response("No files found!", status=400)
    if file and allowed_file(file.filename):
        images = []
        for file in request.files.get('file'):
            images.append(file)
        mixer = InitializeMixer.InitializeMixer(images)
        mixedImage = mixer.getImage()
        DataHolder.images.clear()
        DataHolder.mixedImage.clear()

        return Response(genImg(mixedImage), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return Response("No files found!", status=400)


def genImg(mixedImage):
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + mixedImage + b'\r\n\r\n')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.run(port=8080, debug=False)
