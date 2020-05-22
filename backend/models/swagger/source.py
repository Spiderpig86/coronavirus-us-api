from enum import Enum


class Source(str, Enum):

    NYT = "nyt"
    JHU = "jhu"

    @staticmethod
    def list():
        return list(map(lambda source: source.value, Source))
