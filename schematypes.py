
import abc, jsonschema, IPython, re, json, pathlib, munch, collections, fnmatch, jsonpointer, functools, typing, copy

def merge(*object):
    if not object: return {}
    output = munch.Munch()
    for object in object:
        output.update(object)
    return output
        
class Metatype(abc.ABCMeta):
    def __instancecheck__(cls, object):
        try: return cls.validate(object) or True
        except: return False
        
    def new(cls, **schema):
        return type(schema.get('title', cls.__name__), (cls,), {}, **schema)
        

    def __add__(cls, object, *, key='anyOf'): 
        complex = cls.__schema__.get(key, [cls.__schema__]) + object.__schema__.get(key, [object.__schema__])
        return type(cls.__name__ + object.__name__, (Primitive,), {}, **{key: complex})
        
    def __neg__(cls):
        return type('Not'+cls.__name__, (Primitive,), {}, **{'not': cls.__schema__})
    
    def __sub__(cls, object): return cls + -object
    
    def __mul__(cls, object): 
        schema = item = copy.deepcopy(cls.__schema__)
        while 'items' in item:
            item = schema.get('items')
        item.update(items=object.__schema__)            
        schema.update(title=cls.__name__ + object.__name__)
        return List.new(**schema)
    def __truediv__(): ...
    

        
    __and__ = functools.partialmethod(__add__, key='allOf')
    __or__ = functools.partialmethod(__add__, key='oneOf')
    
    
class Jsonschema(Metatype):
    _metaschema = jsonschema.Draft7Validator.META_SCHEMA
    _format_checker = jsonschema.draft7_format_checker
    def __new__(cls, name, bases, kwargs, **schema):
        self = super().__new__(cls, name, bases, kwargs)
        self.__schema__ = self._build_schema(name, bases, kwargs, schema)
        return self
    
    def _build_schema(self, name, bases, kwargs, schema) -> dict:
        ref = schema.pop('schema', None)
        if ref:
            schema = json.loads(pathlib.Path(ref).read_text())
        complex = {'title': self.__name__}
        if self.__doc__: complex.update(description=self.__doc__)
        for base in self.__mro__:
            complex.update(getattr(base, '__schema__', {}))
        complex.update(schema)
        jsonschema.validate(complex, self._metaschema, format_checker=self._format_checker)
        return complex
        
    def discover(self, object=None):
        for cls in self.__subclasses__():
            if isinstance(cls, DeferDiscover):
                cls.discover(object)
            elif not issubclass(cls, NoDiscover):
                if isinstance(object, cls):
                    return cls.discover(cls(object))
        return object

    def discover_type(self, object=None):
        for cls in self.__subclasses__():
            if issubclass(cls, object):
                return cls
        return object

    def validate(cls, object):
        jsonschema.validate(object, cls.__schema__, format_checker=cls._format_checker)
        
    def __getitem__(cls, object):
        return jsonpointer.resolve_pointer(cls.__schema__, object)
    
class Schema(metaclass=Jsonschema): 
    def __new__(cls, *args, **kwargs):
        args and cls.validate(args[0])
        return super().__new__(cls, *args, **kwargs)
        
 
    
class Integer(Schema, int, type='integer'): ...
class Float(Schema, float, type='number'): ...        
class String(Schema, str, type='string'):
    def pattern(cls, pattern: typing.Union[str], **schema):
        return cls.new(title=pattern, pattern=getattr(pattern, 'pattern', pattern), **schema)
    
    def glob(cls, pattern: typing.Union[str], **schema):
        return cls.pattern(fnmatch.translate(pattern), **schema)

class List(Schema, list, type='array'): 
    @classmethod
    def sized(cls, *length: int):
        if len(length) == 1: return cls.new(title=cls.__name__ + F"[{length[0]}]", minItems=length[0], maxItems=length[0]+1)
        return cls.new(title=cls.__name__ + F"[{length[0]}:{length[1]}]", minItems=length[0], maxItems=length[1])

class Dict(Schema, dict, type='object'): 
    def __new__(cls, *args, **kwargs):
        object = dict(*args, **kwargs)
        return super().__new__(cls, object)
    def __init_subclass__(cls, **schema):
        cls.__schema__.update(**cls._make_properties(**getattr(cls, '__annotations__', {})))

    @classmethod
    def properties(cls, *required, **schema):
        return type(cls.__name__, (Dict,), {}, **cls._make_properties(*required, **schema))
    
    @staticmethod
    def _make_properties(*required, **properties):
        return dict(properties={x: Schema.discover_type(y).__schema__ for x, y in properties.items()}, required=list(required))
        
class DeferDiscover: ...
class NoDiscover: ...


    
class Primitive(Schema, DeferDiscover): 
    def __new__(cls, object=None): return cls.validate(object) or object

class Bool(Primitive, type='boolean'): ...
class Null(Primitive, type='null'): ...
    
    
class Date(String, format="date"): ...
class Time(String, format="time"): ...
class Datetime(String, format="date-time"): ...
class JsonPointer(String, NoDiscover, format="json-pointer"): ...
class IPv4(String, NoDiscover, format="ipv4"): ...
class IPv6(String, NoDiscover, format="ipv6"): ...
class UriTemplate(String, NoDiscover, format="uri-template"): ...
class Color(String, NoDiscover, format="color"): ...
class Email(String, NoDiscover, format="email"): ...
    
import doctest
class URL(String, format="uri"): ...
    
class Composite(Primitive, DeferDiscover): ...
    


class Configurable(Schema):
    def __new__(cls, *args, **kwargs):
        try: # If there is another baseclass try to instantiate it.
            self = super().__new__(cls, *args, **kwargs)
        except:
            self = super().__new__(cls)
            vars(self).update(kwargs)
        cls.validate(vars(self))
        return self
        
    def load_config(self, name, **ac_options):
        vars(self).update(merge(vars(self), anyconfig.load(name, **ac_options)))
        type(self).validate(vars(self))
        return self
    
    
    def __init_subclass__(cls, **schema):
        cls.__schema__ = dict(properties={x: Schema.discover_type(y).__schema__ for x, y in getattr(cls, '__annotations__', {}).items()})
        
        
class Forward(typing.ForwardRef, _root=False):
    ...
class Instance(Forward, _root=False):
    ...
        