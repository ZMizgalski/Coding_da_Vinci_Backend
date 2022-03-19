from picture_mixer import ImageMixer
from servieces import DataHolder


class InitializeMixer:

    def __init__(self, images):
        ImageMixer.ImageMixer(images).start()
