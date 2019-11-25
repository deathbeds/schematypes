#!/usr/bin/env python
# coding: utf-8
from .schemas import String, JsonSchema, discover


class Uri(String, format="uri"):
    def get(self, *args, **kwargs):
        return __import__("requests").get(self, *args, **kwargs)

    def text(self):
        return Uri.get(self).text

    def json(self):
        return Uri.get(self).json()


class Arrow:
    def time(self: String) -> "arrow.Arrow":
        return __import__("arrow").Arrow(self)


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


class Markdown(
    String, pattern=r"^[#|>*|+|-]+\s+", contentMediaType="text/markdown"
):
    def display(self):
        return __import__("IPython").display.Markdown(self)

    def _repr_mimebundle_(self, include=None, exclude=None):
        return (
            __import__("IPython")
            .get_ipython()
            .display_formatter.format(self.display())
        )


class GraphViz(String, pattern=r"^[di]?graph\s{.+}"):
    def graphviz(self):
        return __import__("graphviz").Source(self)

    def _repr_mimebundle_(self, include=None, exclude=None):
        return (
            __import__("IPython")
            .get_ipython()
            .display_formatter.format(self.graphviz())
        )


class File(String, format="file-path"):
    def __init__(self, *a, **k):
        assert __import__("pathlib").Path(self).exists()

    def read_text(self):
        return String.discover(__import__("pathlib").Path(self).read_text())

    def read_json(self):
        with open(self) as file:
            object = __import__("ujson").load(file)
        return object

    def parse(self, *args, **kwargs):
        return discover(__import__("anyconfig").load(self, *args, **kwargs))
