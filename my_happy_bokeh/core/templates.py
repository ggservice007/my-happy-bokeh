'''
Provide Jinja2 templates used by Bokeh to embed Bokeh documents and
models in various ways.

.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_JS
.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_NB_JS
.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_REQUEST_TAG
.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_TAG
.. bokeh-jinja:: bokeh.core.templates.CSS_RESOURCES
.. bokeh-jinja:: bokeh.core.templates.DOC_JS
.. bokeh-jinja:: bokeh.core.templates.DOC_NB_JS
.. bokeh-jinja:: bokeh.core.templates.FILE
.. bokeh-jinja:: bokeh.core.templates.JS_RESOURCES
.. bokeh-jinja:: bokeh.core.templates.NOTEBOOK_LOAD
.. bokeh-jinja:: bokeh.core.templates.PLOT_DIV
.. bokeh-jinja:: bokeh.core.templates.ROOT_DIV
.. bokeh-jinja:: bokeh.core.templates.SCRIPT_TAG

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import json
import requests
import sys
from os.path import dirname, join


# External imports
from jinja2 import Environment, FileSystemLoader, Markup

from ..util import paths

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'AUTOLOAD_JS',
    'AUTOLOAD_NB_JS',
    'AUTOLOAD_REQUEST_TAG',
    'AUTOLOAD_TAG',
    'CSS_RESOURCES',
    'DOC_JS',
    'DOC_NB_JS',
    'FILE',
    'get_env',
    'JS_RESOURCES',
    'MACROS',
    'NOTEBOOK_LOAD',
    'PLOT_DIV',
    'ROOT_DIV',
    'SCRIPT_TAG',
)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

def get_env():
    ''' Get the correct Jinja2 Environment, also for frozen scripts.
    '''
    url = paths.cdn_base_url() + '/bokeh-template-path'

    res_json = requests.post(url).json()

    templates_path = res_json['absolute']

    return Environment(loader=FileSystemLoader(templates_path))

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

_env = get_env()
_env.filters['json'] = lambda obj: Markup(json.dumps(obj))

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

JS_RESOURCES = _env.get_template("js_resources.html")

CSS_RESOURCES = _env.get_template("css_resources.html")

SCRIPT_TAG = _env.get_template("script_tag.html")

PLOT_DIV = _env.get_template("plot_div.html")

ROOT_DIV = _env.get_template("root_div.html")

DOC_JS = _env.get_template("doc_js.js")

DOC_NB_JS = _env.get_template("doc_nb_js.js")

FILE = _env.get_template("file.html")

MACROS = _env.get_template("macros.html")

NOTEBOOK_LOAD = _env.get_template("notebook_load.html")

AUTOLOAD_JS = _env.get_template("autoload_js.js")

AUTOLOAD_NB_JS = _env.get_template("autoload_nb_js.js")

AUTOLOAD_TAG = _env.get_template("autoload_tag.html")

AUTOLOAD_REQUEST_TAG = _env.get_template("autoload_request_tag.html")

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
