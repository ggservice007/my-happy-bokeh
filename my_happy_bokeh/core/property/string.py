'''
Provide the Regex property.
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
import base64
import re

# Bokeh imports
from .primitive import String

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'Regex',
    'Base64String',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Regex(String):
    '''
    Accept strings that match a given regular expression.

    Args:
        default (string or None, optional) :
            A default value for attributes created from this property to
            have (default: None)

        help (str or None, optional) :
            A documentation string for this property. It will be automatically
            used by the :ref:`bokeh.sphinxext.bokeh_prop` extension when
            generating Spinx documentation. (default: None)

        serialized (bool, optional) :
            Whether attributes created from this property should be included
            in serialization (default: True)

        readonly (bool, optional) :
            Whether attributes created from this property are read-only.
            (default: False)

    Example:

        .. code-block:: python

            >>> class RegexModel(HasProps):
            ...     prop = Regex("foo[0-9]+bar")
            ...

            >>> m = RegexModel()

            >>> m.prop = "foo123bar"

            >>> m.prop = "foo"      # ValueError !!

            >>> m.prop = [1, 2, 3]  # ValueError !!

    '''
    def __init__(self, regex, default=None, help=None):
        self.regex = re.compile(regex)
        super().__init__(default=default, help=help)

    def __str__(self):
        return "%s(%r)" % (self.__class__.__name__, self.regex.pattern)

    def validate(self, value, detail=True):
        super().validate(value, detail)

        if not (value is None or self.regex.match(value) is not None):
            msg = "" if not detail else "expected a string matching %r pattern, got %r" % (self.regex.pattern, value)
            raise ValueError(msg)

class Base64String(String):

    def serialize_value(self, value):
        '''
        Encode a ascii string using Base64.

        Args:
            value : a string to encode

        Returns:
            string

        '''
        if isinstance(value, str):
            value = base64.b64encode(value.encode("utf-8")).decode("utf-8")
        return value

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------