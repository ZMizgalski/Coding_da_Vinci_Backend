import threading


class ImageMixer(threading.Thread):

    def __init__(self, images):
        threading.Thread.__init__(self)
        self.images = images

    def run(self):
        self.mixImages()

    def mixImages(self):
        print(self.images)
