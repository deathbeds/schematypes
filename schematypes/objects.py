#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas

import importnb

with importnb.Notebook():
    try:
        from .schemas import Object
    except:
        from schemas import Object


# In[4]:




# In[5]:


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


Pandas.register(pandas.DataFrame), Pandas.register(pandas.Series)


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


# In[6]:


class Test(__import__("unittest").TestCase):
    def test_instances(x):
        ...


# In[7]:


def load_tests(loader, tests, ignore):
    tests.addTests(
        doctest.DocTestSuite(
            importlib.import_module(__name__), optionflags=doctest.ELLIPSIS
        )
    )
    return tests


if __name__ == "__main__":
    import unittest, pytest, jsonschema, importlib, doctest

    unittest.main(argv=" ", exit=False, verbosity=1)


# In[9]:


if __name__ == "__main__":
    get_ipython().system("jupyter nbconvert --to script objects.ipynb")
    get_ipython().system("black objects.py")
    get_ipython().system("pyreverse objects -osvg -pobjects")
    display(__import__("IPython").display.SVG("classes_objects.svg"))
    get_ipython().system("rm classes_objects.svg objects.py")


# In[ ]:
