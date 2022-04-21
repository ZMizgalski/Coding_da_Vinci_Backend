from flask import Flask, Response, request, flash, redirect, send_from_directory, make_response
from flask_cors import cross_origin
import ssl
from app_utils import AppFunctions, AppVariables
from picture_mixer.MixImage import mix_images
import cv2 as cv

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = AppVariables.appSecretKey
ssl._create_default_https_context = ssl._create_unverified_context


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
    firstImage = request.values.get('firstImage')
    secondImage = request.values.get('secondImage')

    if firstImage is None:
        flash('No file part')
        return Response("Key 'firstImage' not found in request!", status=400)

    if secondImage is None:
        flash('No file part')
        return Response("Key 'secondImage' not found in request!", status=400)

    mixed_file = AppFunctions.prepareImagesToMix(firstImage, secondImage)
    # src = data['src']
    # dst = data['dst']
    # print(src, dst)
    retval, buffer = cv.imencode('.jpg', mixed_file)
    response = make_response(buffer.tobytes())
    # return send_from_directory(src, dst, as_attachment=True)
    return response


app.run(port=8080, debug=False)
