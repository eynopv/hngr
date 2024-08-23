from .loaders import FileLoader, RequestLoader


def test_fileloader_not_throwing():
    loader = FileLoader()
    loader.load("./mocks/delish.html")
