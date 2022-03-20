from picture_mixer import ImageMixer


class InitializeMixer:

    def __init__(self, images):
        ImageMixer.ImageMixer(images).start()
