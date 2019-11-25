#!/usr/bin/env python
# coding: utf-8

from .schemas import Object


class Pandas(Object):
    def _repr_mimebundle_(self, include=None, exclude=None):
        data, metadata = super()._repr_mimebundle_(include, exclude)
        return (data, {**metadata, "allOf": []})


# Pandas.register(pandas.DataFrame), Pandas.register(pandas.Series)


class Module(Object):
    def _repr_mimebundle_(self, include=None, exclude=None):
        data, metadata = super()._repr_mimebundle_(include, exclude)
        return (
            data,
            {
                **metadata,
                "title": self.object.__name__,
                "description": self.object.__doc__ or "",
                "@id": getattr(self.object, "__file__", ""),
            },
        )


Module.register(__import__("types").ModuleType)  # pylint: disable=no-member
