#!/usr/bin/env python
# coding: utf-8

# In[6]:


import importnb

with importnb.Notebook():
    try:
        from .schemas import Dict, List
    except:
        from schemas import Dict, List


# In[7]:


class DictofDict(Dict, additionalProperties=Dict.__schema__):
    def graph(x, **kwargs):
        return __import__("networkx").from_dict_of_dicts(x, **kwargs)

    def digraph(x, **kwargs):
        kwargs["create_using"] = kwargs.get(
            "create_using", __import__("networkx").DiGraph()
        )
        return x.graph(**kwargs)


class DictofList(Dict, additionalProperties=List.__schema__):
    def graph(x, **kwargs):
        return __import__("networkx").from_dict_of_lists(x, **kwargs)

    def digraph(x, **kwargs):
        kwargs["create_using"] = kwargs.get(
            "create_using", __import__("networkx").DiGraph()
        )
        return x.graph(**kwargs)


# In[8]:


class Test(__import__("unittest").TestCase):
    def test_instances(x):
        ...


# In[9]:


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


# In[12]:


if __name__ == "__main__":
    get_ipython().system("jupyter nbconvert --to script dicts.ipynb")
    get_ipython().system("black dicts.py")
    get_ipython().system("pyreverse dicts -osvg -pdicts")
    display(__import__("IPython").display.SVG("classes_dicts.svg"))
    get_ipython().system("rm classes_dicts.svg dicts.py")


# In[ ]:
