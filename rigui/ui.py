from maya import cmds

print "UI"

def rigArm(*args):
  #from rig import arm_rig
  #reload(arm_rig)
  import rig.arm_rig as rig_arm
  print rig_arm
  rig_arm = rig_arm.Rig_Arm()
  print rig_arm
  rig_arm.rig_arm()

  #rig_arm = Rig_Arm()
  #rig_arm.rig_arm()

mymenu = cmds.menu('RDojo_Menu',label='RDMenu',to=True,p="MayaWindow")
cmds.menuItem(label="Rig_Arm",p=mymenu,command=rigArm)

