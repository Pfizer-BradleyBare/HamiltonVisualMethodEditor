from ....Tools.AbstractClasses import ObjectABC


class MoveToTrackNumberOptions(ObjectABC):
    def __init__(self, Name: str, Track: int):

        self.Name: str = Name

        self.Track: int = Track

    def GetName(self) -> str:
        return self.Name
