import wget
import os
from app_utils.AppVariables import *
import shutil
from datetime import datetime
import uuid
from picture_mixer import MixImage
from picture_mixer.MixImage import mix_images


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def prepareImagesToMix(firstImage, secondImage):
    makeDir(tmpImagesFolder)
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = tmpImagesFolder + '\\' + date + "_" + secretWorkingDirectoryKey
    makeDir(path)

    print(len(firstImage.split("/")))

    firstExtension = firstImage.split("/")[len(firstImage.split("/")) - 1].split('.')[1]
    secondExtension = secondImage.split("/")[len(secondImage.split("/")) - 1].split('.')[1]
    uuid2 = str(uuid.uuid4())
    firstFile = uuid2 + '_1_.' + firstExtension
    secondFile = uuid2 + '_2_.' + secondExtension

    downloadImage(firstImage, path + '\\' + firstFile)
    downloadImage(secondImage, path + '\\' + secondFile)
    mixed_file = mix_images(path + '\\' + firstFile, path + '\\' + secondFile)
    # os.rename(path, tmpImagesFolder + '\\' + date + "_" + secretDoneDirectoryKey)
    shutil.rmtree(path, ignore_errors=True)
    # print(path, tmpImagesFolder + '\\' + date + "_" + secretDoneDirectoryKey)
    # mixedFileName = mixImage(firstFile, uuid2, path, firstExtension, date)
    return mixed_file


def generateImage(path):
    finalPath = MixImage.MixImage(path)
    print(finalPath)


def downloadImage(URL, Path):
    return wget.download(URL, Path)


def makeDir(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def clear_directory(Path):
    for filename in os.listdir(Path):
        file_path = os.path.join(Path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif len(os.listdir(file_path)) == 0:
                shutil.rmtree(file_path)
            elif os.path.isdir(file_path) & (secretDoneDirectoryKey in filename):
                shutil.rmtree(file_path)
            else:
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
