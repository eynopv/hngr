from .loaders import FileLoader, TextLoader


def test_fileloader_not_throwing():
    loader = FileLoader()
    loader.load("./mocks/delish.html")


def test_textloader_returns_source():
    loader = TextLoader()
    result = loader.load("loaded content")
    assert result == "loaded content"
