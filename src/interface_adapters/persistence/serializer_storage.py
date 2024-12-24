import pickle

from src.application.interfaces import Savable, GetAllRepository


class SerializerStorage[Object](Savable[Object], GetAllRepository[Object]):
    def __init__(self, destination: str) -> None:
        self._destination = destination

    async def save(self, one_object: Object) -> None:
        with open(self._destination, 'wb') as file:
            pickle.dump([one_object], file)

    async def save_multiple(self, objects: list[Object]) -> None:
        with open(self._destination, 'wb') as file:
            pickle.dump(objects, file)

    async def get_all(self) -> list[Object]:
        with open(self._destination, 'rb') as file:
            data = pickle.load(file)
            if not isinstance(data, list):
                raise ValueError("Data is not a list")
            return data
