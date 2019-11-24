#!/usr/bin/env python
# coding: utf-8
from .schemas import String, JsonSchema, discover

class Uri(String, format="uri"):
    def get(x, *args, **kwargs):
        return __import__("requests").get(x, *args, **kwargs)

    def text(x):
        return Uri.get(x).text

    def json(x):
        return get(x).json()


class Arrow:
    def time(x: String) -> "arrow.Arrow":
        return __import__("arrow").Arrow(x)


class Date(Arrow, String, format="date"):
    ...


class Datetime(Arrow, String, format="date-time"):
    ...


class Time(Arrow, String, format="time"):
    ...


class Email(String, format="email"):
    ...


class JsonPointer(String, format="json-pointer"):
    ...



class Markdown(String, pattern=r"^[#|>*|+|-]+\s+", contentMediaType='text/markdown'):
    def display(x):
        return __import__("IPython").display.Markdown(x)

    def _repr_mimebundle_(x, include=None, exclude=None):
        return __import__("IPython").get_ipython().display_formatter.format(x.display())


class GraphViz(String, pattern=r"^[di]?graph\s{.+}"):
    def graphviz(x):
        return __import__("graphviz").Source(x)

    def _repr_mimebundle_(x, include=None, exclude=None):
        return (
            __import__("IPython").get_ipython().display_formatter.format(x.graphviz())
        )


class File(String, format="file-path"):
    def __init__(x, *a, **k):
        assert __import__("pathlib").Path(x).exists()

    def read_text(x):
        return String.discover(__import__("pathlib").Path(x).read_text())

    def read_json(x):
        with open(x) as file:
            object = __import__("ujson").load(file)
        return object

    def parse(x, *args, **kwargs):
        return discover(__import__("anyconfig").load(x, *args, **kwargs))