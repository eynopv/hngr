from abc import ABC, abstractmethod
import httpx
from playwright.sync_api import sync_playwright


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


class TextLoader(Loader):

    @staticmethod
    def load(source: str) -> str:
        return source


class RequestLoader(Loader):

    @staticmethod
    def load(source: str):
        response = httpx.get(source)
        return response.text


class BrowserLoader(Loader):

    @staticmethod
    def load(source: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()
            page.goto(source)
            content = page.content()
            browser.close()
            return content
