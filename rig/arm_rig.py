from maya import cmds

def createJointChain(chainType):
    cmds.joint(n='C_arm'+chainType+"_JNT",p=[3, 0, 3])
    cmds.joint(n='C_elbow'+chainType+'_JNT',p=[0, 0,0])
    cmds.joint ('C_arm'+chainType+'_JNT',e=True, zso=True,oj='xyz',sao='yup');
    cmds.joint(n='C_wrist'+chainType+'_JNT',p=[1,0 ,-4])
    cmds.joint ('C_elbow'+chainType+'_JNT',e=True, zso=True,oj='xyz',sao='yup');
    cmds.joint(n='C_wrist'+chainType+'End_JNT',p=[0,0,-7])
    cmds.joint ('C_wrist'+chainType+'End_JNT',e=True, zso=True,oj='xyz',sao='yup');
    cmds.select(d=True)
  

def circleControl(name):
    circleCtl = cmds.circle(n=name, ch=0, o=1, nr = [1,0,0])[0]
    return circleCtl

"""
create joint chains
"""

createJointChain("Bind")
createJointChain("IK")
createJointChain("FK")

"""Create IK Rig"""
#Create Ik handle
armIkHandle = cmds.ikHandle(n='L_arm_IKH', sj='C_armIK_JNT',ee='C_wristIK_JNT',sol="ikRPsolver",p=2,w=True)
#get world space potition of wrist joint
pos = cmds.xform('C_wristIK_JNT',q=True,t=True,ws=True)
#create empty group
IKoffGrp = cmds.group(empty=1, n=('C_wristIKOffset_GRP'))
#create circle control onject
#IKcircleCtl = cmds.circle(n="L_wristIK_CTL",nr=(0,0,1),c=(0,0,0))
IKcircleCtl = circleControl("L_wristIK_CTL")
cmds.parent(IKcircleCtl ,IKoffGrp)
parCon = cmds.parentConstraint('C_wristIK_JNT', IKoffGrp, mo=0)
cmds.delete(parCon)
#parent Ik to control
cmds.parent('L_arm_IKH',"L_wristIK_CTL")

"""Create FK Rig"""
jntName = 'C_arm'
circleCtl = circleControl(jntName+"FK_CTL")

jntSel = cmds.select( 'C_armFK_JNT',r=True)

#jntName = jntSel[0].split("_JNT")
#ctl = circleCtl

#controlCircle = cmds.rename(ctl, (jntName + "FK_CTL"))

cmds.select(cl=1)

offGrp = cmds.group(empty=1, n=(jntName + "FKOffset_GRP"))

cmds.parent(circleCtl ,offGrp)

parCon = cmds.parentConstraint('C_armFK_JNT', offGrp, mo=0)

cmds.delete(parCon)
#Connect IK and FK to Rig joints