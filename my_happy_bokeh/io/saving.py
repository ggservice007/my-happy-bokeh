'''

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
from os.path import abspath
from pathlib import Path
from warnings import warn
import ujson

# Bokeh imports
from ..settings import settings
from .state import curstate
from .util import default_filename


#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

DEFAULT_TITLE = "Bokeh Plot"

__all__ = (
    'save',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

def save(obj, filename=None, resources=None, title=None, template=None, state=None, **kwargs):
    ''' Save an HTML file with the data for the current document.

    Will fall back to the default output state (or an explicitly provided
    :class:`State` object) for ``filename``, ``resources``, or ``title`` if they
    are not provided. If the filename is not given and not provided via output state,
    it is derived from the script name (e.g. ``/foo/myplot.py`` will create
    ``/foo/myplot.html``)

    Args:
        obj (LayoutDOM object) : a Layout (Row/Column), Plot or Widget object to display

        filename (str, optional) : filename to save document under (default: None)
            If None, use the default state configuration.

        resources (Resources, optional) : A Resources config to use (default: None)
            If None, use the default state configuration, if there is one.
            otherwise use ``resources.INLINE``.

        title (str, optional) : a title for the HTML document (default: None)
            If None, use the default state title value, if there is one.
            Otherwise, use "Bokeh Plot"

        template (Template, optional) : HTML document template (default: FILE)
            A Jinja2 Template, see bokeh.core.templates.FILE for the required template
            parameters

        state (State, optional) :
            A :class:`State` object. If None, then the current default
            implicit state is used. (default: None).

    Returns:
        str: the filename where the HTML file is saved.

    '''

    if state is None:
        state = curstate()

    theme = state.document.theme

    filename, resources, title = _get_save_args(state, filename, resources, title)

    file_url = _save_helper(obj, filename, resources, title, template, theme)
    return {
        'file_url': file_url,
        'file_abs_path': abspath(filename)
    }

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

def _get_save_args(state, filename, resources, title):
    '''

    '''
    filename, is_default_filename = _get_save_filename(state, filename)

    resources = _get_save_resources(state, resources, is_default_filename)

    title = _get_save_title(state, title, is_default_filename)

    return filename, resources, title

def _get_save_filename(state, filename):
    if filename is not None:
        return filename, False

    if state.file and not settings.ignore_filename():
        return state.file['filename'], False

    return default_filename("html"), True

def _get_save_resources(state, resources, suppress_warning):
    if resources is not None:
        return resources

    if state.file:
        return state.file['resources']

    if not suppress_warning:
        warn("save() called but no resources were supplied and output_file(...) was never called, defaulting to resources.CDN")

    from ..resources import Resources
    return Resources(mode=settings.resources())

def _get_save_title(state, title, suppress_warning):
    if title is not None:
        return title

    if state.file:
        return state.file['title']

    if not suppress_warning:
        warn("save() called but no title was supplied and output_file(...) was never called, using default title 'Bokeh Plot'")

    return DEFAULT_TITLE

def _save_helper(obj, filename, resources, title, template, theme=None):
    '''

    '''
    from ..embed import file_html
    directory_info = resources.get_public_work_directory_info()
    file_path = Path(filename)
    directory_path = Path(directory_info['path'], file_path.parent)
    directory_path.mkdir(parents=True, exist_ok=True)

    html_info = file_html(obj, resources, filename, title=title, template=template, theme=theme)

    with open(Path(directory_path, file_path.stem + '.json'),
              mode="w", encoding="utf-8") as f:
        f.write(ujson.dumps(html_info['docs_json']))

    with open(Path(directory_path, file_path.stem + '.js'),
              mode="w", encoding="utf-8") as f:
        f.write(html_info['script'].strip())

    with open(Path(directory_info['path'], filename), mode="w", encoding="utf-8") as f:
        f.write(html_info['all_html_content'].strip())

    file_url = directory_info['url'] + '/' + filename

    return file_url

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
