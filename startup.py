import maya.cmds as cmds
import os
print "Startup"


os.environ["RDOJO_DATA"] = 'D:/GitRepositories/Python101/data/'
import rigui.ui as ui
reload(ui)
