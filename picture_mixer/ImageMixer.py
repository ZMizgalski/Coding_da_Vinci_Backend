import threading
from picture_mixer.servieces import DataHolder


class ImageMixer(threading.Thread):

    def __init__(self, images):
        self.images = images
        threading.Thread.__init__(self)

    def run(self):
        self.mixImages()

    def mixImages(self):
        DataHolder.images = self.images
        DataHolder.mixedImage.append(self.images[0])
