from abc import ABC, abstractmethod
import httpx


class Loader(ABC):

    @staticmethod
    @abstractmethod
    def load(source: str) -> str:
        pass


class FileLoader(Loader):

    @staticmethod
    def load(source: str):
        with open(source, "r") as reader:
            return reader.read()


class RequestLoader(Loader):

    @staticmethod
    def load(source: str):
        response = httpx.get(source)
        return response.text
