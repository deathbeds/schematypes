#!/usr/bin/env python
# coding: utf-8

from .schemas import Dict, List

class DictofDict(Dict, additionalProperties=Dict.__schema__): ...

class DictofList(Dict, additionalProperties=List.__schema__): ...
class Test(__import__("unittest").TestCase):
    def test_instances(x):...
        
# class NbFormat(Dict, **__import__('nbformat').validator._get_schema_json(nbformat.v4)): 
#     __context__ = 'https://raw.githubusercontent.com/jupyter/nbformat/master/nbformat/v4/nbformat.v4.schema.json#/'

# class JsonPatch(List, **requests.get("http://json.schemastore.org/json-patch").json()):
#     def __call__(self, object): return Type.discover(__import__('jsonpatch').apply_patch(object, self))
# class TableSchema(Dict, **requests.get("https://frictionlessdata.io/schemas/table-schema.json").json()): ...
# class GeoJson(Dict, **requests.get("http://json.schemastore.org/geojson").json()): ...
