from pathlib import Path

from src.application.interfaces import Savable


class PlainTextRepository(Savable[str]):
    def __init__(self, destination: Path) -> None:
        self._destination = destination

    async def save(self, one_object: str) -> None:
        with open(self._destination, 'w') as file:
            file.write(one_object)

    async def save_multiple(self, objects: list[str]) -> None:
        file_names = [self._destination.parent / f"{self._destination.name}_{i}.txt" for i in range(len(objects))]
        for file_name, obj in zip(file_names, objects):
            with open(file_name, 'w') as file:
                file.write(obj)
