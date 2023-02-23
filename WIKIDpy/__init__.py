''' Top level init file for WIKIDpy, sets defaults''' 


#internal modules
from . import readscan
from . import base

from .base import *

__all__=["base"] # all routines which will be imported with *

#import configuration file for location of data etc.
#confFile='/users/sdicker/WIKIDpy/WIKIDpy/defaults.conf'
confFile='WIKIDpy/defaults.conf'
readConfig(confFile)

#Are we at GBO (or whereever conf file points)?
chkLocation() #ignore return value
