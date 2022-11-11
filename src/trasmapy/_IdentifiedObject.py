class IdentifiedObject:
    def __init__(self, id: str) -> None:
        self._id = id

    @property
    def id(self) -> str:
        return self._id
