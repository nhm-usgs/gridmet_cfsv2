from .gridmet_cfsv2 import Gridmet
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['Gridmet', ]
