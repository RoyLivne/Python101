from maya import cmds
from  system import utils
import json
import os
import system.utils as utils

"""
Old values before sending to json file
    rig_data= {}
    
    FkJoints = ["C_armFK_JNT","C_elbowFK_JNT","C_wristFK_JNT"]
    ikJoints = [['C_armIK_JNT',[3,0,3]],['C_elbowIK_JNT',[0,0,0]],['C_wristIK_JNT',[1,0,-4]]]
    FkControlInfo = [[FkJoints[0],'C_armFK_CTL','C_armFKOffset_GRP'],[FkJoints[1],'C_elbowFK_CTL','C_elbowFKOffset_GRP'],[FkJoints[2],'C_wristFK_CTL','C_wristFKOffset_GRP']]
    
    rig_data['FkJoints'] = ["C_armFK_JNT","C_elbowFK_JNT","C_wristFK_JNT"]
    rig_data['ikJoints'] = [['C_armIK_JNT',[3,0,3]],['C_elbowIK_JNT',[0,0,0]],['C_wristIK_JNT',[1,0,-4]]]
    rig_data['positions'] = [[3, 0, 3],[0, 0,0],[1,0 ,-4],[0,0,-7]]
"""
class Rig_Arm:
    def __init__(self):
        #Get our joint lists from a json file
        data_path = os.environ["RDOJO_DATA"] + '/arm.json'
        #Use our readJson function
        data = utils.readJson(data_path)
        #Load the json into a dictionary
        self.module_info = json.loads(data)

    def rig_arm(self):
        """
        create joint chains
        """
        self.createJointChain("Bind")
        self.createJointChain("IK")
        self.createJointChain("FK")

        print "chains created"

        """Create IK Rig"""
        ikh = self.createIkHandle("")

        print "Ik handle created"

        """Create FK Rig"""
        self.createFKControls("")

        print "Fk controls created"

        pvpos = self.calculatePVPosition(self.module_info['ikJoints'])
        pvCtrlInfo = [[pvpos, 'C_armPV_CTRL', 'C_armPV_GRP']]
        self.createPVControl(pvCtrlInfo)
        cmds.poleVectorConstraint(pvCtrlInfo[0][1], ikh[0])

        print "PV created"

        cmds.orientConstraint('L_wristIK_CTL', self.module_info['ikJoints'][2][0], mo=True)
        cmds.parent(FkControlInfo[1][2], FkControlInfo[0][1])
        cmds.parent(FkControlInfo[2][2], FkControlInfo[1][1])
        cmds.orientConstraint(FkControlInfo[0][1], self.module_info['FkJoints'][0])
        cmds.orientConstraint(FkControlInfo[1][1], self.module_info['FkJoints'][1])
        cmds.orientConstraint(FkControlInfo[2][1], self.module_info['FkJoints'][2])
        print "Orient constrainted"

    def createJointChain(self,chainType):
        cmds.joint(n='C_arm'+chainType+"_JNT",p=self.module_info['positions'][0])
        cmds.joint(n='C_elbow'+chainType+'_JNT',p=self.module_info['positions'][1])
        cmds.joint ('C_arm'+chainType+'_JNT',e=True, zso=True,oj='xyz',sao='yup');
        cmds.joint(n='C_wrist'+chainType+'_JNT',p=self.module_info['positions'][2])
        cmds.joint ('C_elbow'+chainType+'_JNT',e=True, zso=True,oj='xyz',sao='yup');
        cmds.joint(n='C_wrist'+chainType+'End_JNT',p=self.module_info['positions'][3])
        cmds.joint ('C_wrist'+chainType+'End_JNT',e=True, zso=True,oj='xyz',sao='yup');
        cmds.select(d=True)


    def circleControl(self,name):
        circleCtl = cmds.circle(n=name, ch=0, o=1, nr = [1,0,0])[0]
        return circleCtl

    """Create IK Rig"""
    def createIkHandle(self,*args):
        #Create Ik handle
        armIkHandle = cmds.ikHandle(n='L_arm_IKH', sj='C_armIK_JNT',ee='C_wristIK_JNT',sol="ikRPsolver",p=2,w=True)
        #get world space potition of wrist joint
        pos = cmds.xform('C_wristIK_JNT',q=True,t=True,ws=True)
        #create empty group
        IKoffGrp = cmds.group(empty=1, n=('C_wristIKOffset_GRP'))
        #create circle control onject
        #IKcircleCtl = cmds.circle(n="L_wristIK_CTL",nr=(0,0,1),c=(0,0,0))
        IKcircleCtl = self.circleControl("L_wristIK_CTL")
        cmds.parent(IKcircleCtl ,IKoffGrp)
        parCon = cmds.parentConstraint('C_wristIK_JNT', IKoffGrp, mo=0)
        cmds.delete(parCon)
        #parent Ik to control
        cmds.parent('L_arm_IKH',"L_wristIK_CTL")
        return armIkHandle

    def createFKControls(self,*args):
        for fkc in self.module_info['FkJoints']:
            name = fkc.replace("_JNT","")+"_CTL"
            circleCtl =  self.circleControl(name);
            cmds.select(fkc, r=True)
            cmds.select(cl=1)
            offGrp = cmds.group(empty=1, n=(fkc.replace("_JNT","") + "Offset_GRP"))
            cmds.parent(circleCtl, offGrp)
            parCon = cmds.parentConstraint(fkc, offGrp, mo=0)
            cmds.delete(parCon)

    def createPVControl(self,povCtrlInfo):
        for info in povCtrlInfo:
            pos = info[0]
            ctrlGrp = cmds.group(em=True, name = info[2])
            ctrl = self.circleControl(info[1])
            cmds.parent(ctrl,ctrlGrp)
            cmds.xform(ctrlGrp,t=pos,ws=True)

    def calculatePVPosition(self,jnts):
        from maya import cmds,OpenMaya
        start = cmds.xform(jnts[0][0],q=True,ws=True,t=True)
        mid = cmds.xform(jnts[1][0],q=True,ws=True,t=True)
        end = cmds.xform(jnts[2][0], q=True, ws=True, t=True)
        startv= OpenMaya.MVector(start[0],start[1],start[2])
        midv = OpenMaya.MVector(mid[0],mid[1],mid[2])
        endv = OpenMaya.MVector(end[0],end[1],end[2])
        startEnd  = endv - startv
        startMid = midv - startv
        dotP = startMid * startEnd
        proj = float(dotP)/float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV *= 0.5
        finalV = arrowV +midv
        return([finalV.x,finalV.y,finalV.z])




