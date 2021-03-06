'''
Provide classes for representing RGB(A) and HSL(A) colors, as well as
define common named colors.

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Bokeh imports
from . import groups, named
from .color import Color
from .hsl import HSL
from .rgb import RGB

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'Color',
    'HSL',
    'RGB',
    'groups',
    'named',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
