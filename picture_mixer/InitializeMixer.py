from picture_mixer import ImageMixer
from picture_mixer.servieces import DataHolder


class InitializeMixer:

    def __init__(self, images):
        self.threads = []
        self.threads.append(ImageMixer.ImageMixer(images))
        self.setupMixer()

    def startThreads(self):
        for thread in self.threads:
            thread.start()

    def waitTillFinished(self):
        for thread in self.threads:
            thread.join()

    def setupMixer(self):
        self.startThreads()
        self.waitTillFinished()

    @staticmethod
    def getImage():
        return DataHolder.mixedImage[0]
