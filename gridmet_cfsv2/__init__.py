
from ._version import get_versions
from .gridmet_cfsv2 import Gridmet
from .helpers import np_get_wval, getaverage
__version__ = get_versions()['version']
del get_versions
