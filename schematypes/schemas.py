#!/usr/bin/env python
# coding: utf-8

import abc
import collections
import dataclasses
import gc
import importlib
import json
import sys
import typing

import jsonschema


class Garbage:
    def num_refs(self):
        return gc.collect() and sys.getrefcount(self)

    def referrers(self):
        return gc.collect() and gc.get_referrers(self)

    def referents(self):
        return gc.collect() and gc.get_referents(self)

    def find(self, ns="__main__"):
        hash = id(self)
        return {
            k
            for k, v in vars(
                importlib.import_module(ns) if isinstance(ns, str) else ns
            ).items()
            if id(v) == hash
        }

    def type(self):
        return type(self)


class JsonSchemaType(abc.ABCMeta, Garbage):
    __meta_schema__ = jsonschema.Draft7Validator.META_SCHEMA

    def __new__(cls, name, base, kwargs, **schema):
        """Create a new JsonSchemaType type.  Validate the schema on the metaschema. x"""
        self = super().__new__(cls, name, base, kwargs)
        self.__schema__ = dict(
            collections.ChainMap(
                schema,
                *(getattr(cls, "__schema__", {}) for cls in self.__mro__),
            )
        )
        self.validate_meta_schema(self.__schema__)
        return self

    @classmethod
    def validate_meta_schema(cls, object):
        jsonschema.validate(
            object,
            cls.__meta_schema__,
            format_checker=jsonschema.draft7_format_checker,
        )

    def __instancecheck__(self, object):
        try:
            return (
                jsonschema.validate(
                    object,
                    self.__schema__,
                    format_checker=jsonschema.draft7_format_checker,
                )
                or True
            )
        except:
            return False

    def discover(self, object=None, **schema):
        """Traverse the type module resolution order to discover
        a most compact type representation.

        >>> assert isinstance(JsonSchema.discover(10), int)
        """
        for cls in self.__subclasses__():
            try:
                return cls.discover(cls(getattr(object, "object", object)))
            except BaseException:
                ...
        return object

    def new(self, **schema):
        schema = {
            **self.__schema__,
            **(object if isinstance(object, dict) else {}),
            **schema,
        }
        return type(
            schema.get("title", __import__("json").dumps(schema)),
            (self,),
            {},
            **schema,
        )

    def example(self):
        """Generate an example value of the schema.

        >>> assert isinstance(Integer.example(), int)
        
        This feature requires `hypothesis_jsonschema `

            pip install hypothesis_jsonschema 
        """
        return (
            __import__("hypothesis_jsonschema")
            .from_schema(self.__schema__)
            .example()
        )


class JsonSchema(Garbage, metaclass=JsonSchemaType):
    __context__ = (
        f"{jsonschema.Draft7Validator.META_SCHEMA['$schema']}/properties/"
    )

    def __new__(cls, *args, **kwargs):
        args and cls.validate(args[0])
        return super().__new__(cls, *args, **kwargs)

    def __repr__(self):
        return self.dumps()

    def dumps(self, *args, **kwargs):
        return __import__("ujson").dumps(self, *args, **kwargs)

    @classmethod
    def validate(cls, object):
        assert isinstance(object, cls)


discover = JsonSchema.discover


class List(JsonSchema, list, type="array"):
    def __new__(cls, *args, **kwargs):
        if isinstance(args[0], tuple):
            args = (list(args[0]),) + args[1:]
        return super().__new__(cls, *args, **kwargs)


class Dict(JsonSchema, dict, type="object"):
    def __new__(cls, *args, **kwargs):
        args, kwargs = ({**(args and args[0] or {}), **kwargs},), {}
        return super().__new__(cls, *args, **kwargs)

    def __init_subclass__(cls, **schema):
        cls.__schema__.update(schema)  # pylint: disable=no-member
        if getattr(cls, "__annotations__", {}):
            cls.__schema__.update(  # pylint: disable=no-member
                properties={
                    key: value.__schema__
                    for key, value in getattr(
                        cls, "__annotations__", {}
                    ).items()
                    if hasattr(value, "__schema__")
                }
            )
        cls.validate_meta_schema(cls.__schema__)  # pylint: disable=no-member


class String(JsonSchema, str, type="string"):
    def parse(self, *args, **kwargs):
        """Generate an example value of the schema.

        >>> assert isinstance(Integer.example(), int)
        
        This feature requires `anyconfig`

            pip install anyconfig 
        """
        return JsonSchema.discover(
            __import__("anyconfig").loads(self, *args, **kwargs)
        )

    def json(self):
        return __import__("ujson").loads(self)


class Integer(JsonSchema, int, type="integer"):
    ...


class Number(JsonSchema, float, type="number"):
    ...


class Boolean(JsonSchema, type="boolean"):
    def __new__(cls, object=None, *args, **kwargs):
        cls.validate(object)
        return object


class Null(JsonSchema, type="null"):
    def __new__(cls, object=None, *args, **kwargs):
        return cls.validate(object)


class Object(JsonSchema):
    """Use abc registration to connect to python types."""

    __context__ = None
    object: None

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self.__init__(*args, **kwargs)
        return self

    def __post_init__(self):
        self.object = getattr(self, "object", self.object)
        assert isinstance(self.object, type(self))

    def _repr_mimebundle_(self, include=None, exclude=None, **metadata):
        return {}, metadata


dataclasses.dataclass(Object)
