class IdentifiedObject:
    def __init__(self, id: str) -> None:
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
