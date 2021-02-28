import daiquiri


class Log:
    def __init__(self):
        daiquiri.setup(outputs=(
            daiquiri.output.File(directory="./log"),
        ))

    @staticmethod
    def get_daiquiri():
        return daiquiri.getLogger()