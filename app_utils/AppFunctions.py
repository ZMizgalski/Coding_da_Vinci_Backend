import wget
import os
from app_utils.AppVariables import *
import shutil
from datetime import datetime
import uuid
from picture_mixer.MixImage import mix_images


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def prepareImagesToMix(firstImage, secondImage):
    makeDir(tmpImagesFolder)
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = tmpImagesFolder + '\\' + date
    makeDir(path)
    firstExtension = firstImage.split("/")[len(firstImage.split("/")) - 1].split('.')[1]
    secondExtension = secondImage.split("/")[len(secondImage.split("/")) - 1].split('.')[1]
    uuid2 = str(uuid.uuid4())
    firstFile = uuid2 + '_1_.' + firstExtension
    secondFile = uuid2 + '_2_.' + secondExtension
    downloadImage(firstImage, path + '\\' + firstFile)
    downloadImage(secondImage, path + '\\' + secondFile)
    mixed_file = mix_images(path + '\\' + firstFile, path + '\\' + secondFile)
    shutil.rmtree(path, ignore_errors=True)
    return mixed_file


def downloadImage(URL, Path):
    return wget.download(URL, Path)


def makeDir(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
