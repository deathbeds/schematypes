#!/usr/bin/env python
# coding: utf-8

from .schemas import Object
class Pandas(Object):
    def _repr_mimebundle_(x, include=None, exclude=None):
        data, metadata = super()._repr_mimebundle_(include, exclude)
        return (
            data,
            {
                **metadata,
                "allOf": [
                    TableSchema(
                        __import__("json").loads(x.object.to_json(orient="table"))[
                            "schema"
                        ]
                    ),
                    List.new(minItems=len(x.object), maxItems=len(x.object)).__schema__,
                ],
            },
        )


#Pandas.register(pandas.DataFrame), Pandas.register(pandas.Series)


class Module(Object):
    def _repr_mimebundle_(x, include=None, exclude=None):
        data, metadata = super()._repr_mimebundle_(include, exclude)
        return (
            data,
            {
                **metadata,
                "title": x.object.__name__,
                "description": x.object.__doc__ or "",
                "@id": getattr(x.object, "__file__", ""),
            },
        )


Module.register(__import__("types").ModuleType)
