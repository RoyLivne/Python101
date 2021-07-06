import os
import sys

from maya import cmds

print 'In User Setup'

sys.path.append('D:/GitRepositories/Python101/')

cmds.evalDeferred('import startup')