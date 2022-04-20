class MixImage:

    def __init__(self, path):
        self.path = path

    def mix(self):
        print(self.path)

    def __repr__(self):
        return self.path
