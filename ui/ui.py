from maya import cmds

def rigArm(*args):
  from rig import arm_rig

mymenu = cmds.menu('RDojo_Menu',label='RDMenu',to=True,p="MayaWindow")
cmds.menuItem(label="Rig_Arm",p=mymenu,command=rigArm)



print "UI"

