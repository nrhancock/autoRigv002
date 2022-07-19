# ik/fk arm auto rig v002
# Nate Hancock
# created 6/14/2022
#last update  07/19/2022

from maya import cmds, OpenMaya
import pymel.core as pm
import maya.mel as mel
import math



print("Initializing...")




debug = False
class armRig:
    print("Class call successful")

    def __init__(self, namespace=None):
        if namespace!=None:
            self.namespace=namespace+':'
        else:
            self.namespace=None


        self.window = None
        self.windowsName = ('armrig_UI')
        self.title = ('arm auto rigger')

        UI_created = self.create_arm_ui()
        print ('call UI')

    def create_arm_ui(self):

        if pm.window(self.windowsName, ex=True):
            pm.deleteUI(self.windowsName)

        window = cmds.window(self.windowsName, mm=True, bgc=(0.0, 0.1, 0.1))
        cmds.rowColumnLayout(nc=2)
        global asymmetrical_checked
        asymmetrical_checked = pm.checkBox(value=False, label='Asymmetrical Placement')
        global symmetrical_checked
        symmetrical_checked = pm.checkBox(value=False, label='Symmetrical Placement')

        # if pm.checkBox(symmetrical_checked, query=True, value=True):
        #     pm.checkBox(asymmetrical_checked, value=False)
        # if pm.checkBox(asymmetrical_checked, query=True, value=True):
        #     pm.checkBox(symmetrical_checked, value=False)

        cmds.columnLayout('Main', cal='left')
        global locator_created
        locator_created= cmds.button(w=300, ebg=True, bgc=(0, 0, 0), l='Create Locators for Arm Joint Placement', c=self.create_arm_locators)
        cmds.button(w=300, ebg=True, bgc=(0, 0, 0), l='Create Joints Based on Generated Locators', c=lambda *args: self.create_joints_on_locators(arm_position_locator))
        cmds.button(w=300, ebg=True, bgc=(0, 0, 0), l='Create Joints Based on Selections')

        print(locator_created)
        cmds.showWindow(self.windowsName)

        return (locator_created)


    def l_nrhautofk(self):
        pm.select('l_shoulder_fk','l_elbow_fk','l_wrist_fk')

        joint_chain = pm.ls(sl=True, dag=True)
        last_icon = None
        control_icons = []
        for current_joint in joint_chain[0:-1]:
            print (current_joint)
            current_icon = pm.circle(radius=4, normal=[1, 0, 0])[0]
            local_pad = pm.group()
            waste_icon = pm.parentConstraint(current_joint, local_pad)
            pm.delete(waste_icon)

            if last_icon:
                pm.parent(local_pad, last_icon)

            #connect the control back to the joint
            pm.orientConstraint(current_icon, current_joint)

            last_icon = current_icon

            control_icons.append(current_icon)

        pm.select(control_icons, r=True)

    def r_nrhautofk(self):
        pm.select(cl=True)
        pm.select('r_shoulder_fk', 'r_elbow_fk', 'r_wrist_fk')

        joint_chain = pm.ls(sl=True, dag=True)
        last_icon = None
        control_icons = []
        for current_joint in joint_chain[0:-1]:
            print(current_joint)
            current_icon = pm.circle(radius=4, normal=[1, 0, 0])[0]
            local_pad = pm.group()
            waste_icon = pm.parentConstraint(current_joint, local_pad)
            pm.delete(waste_icon)

            if last_icon:
                pm.parent(local_pad, last_icon)

            # connect the control back to the joint
            pm.orientConstraint(current_icon, current_joint)

            last_icon = current_icon

            control_icons.append(current_icon)

        pm.select(control_icons, r=True)

    '''cleans up an object'''
    def nrh_cleanup(self, obj):
        # delete object history
        deleteHistory = cmds.delete(constructionHistory=True)
        # freeze objects transforms
        freezeTransforms = cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        # center pivot
        sel = cmds.ls(selection=True)
        for obj in sel:
            cmds.xform(obj, centerPivots=True)

    def checkbox_evalutaion(self):
        global asymmetrical_checked
        global symmetrical_checked
        asym_check = pm.checkBox(asymmetrical_checked, query=True, value=True)
        sym_check = pm.checkBox(symmetrical_checked, query=True, value=True)

        if asym_check:
            print('You have checked the Asymmetrical option')
        elif sym_check:
            print('You have checked the Symmetrical option')
        '''Will add an else that automatically makes the system mirrored if nothing is checked at the start'''

    '''start off by creating 4 locators that are parented to a locators
    these locators will be for placing joints and will replaced with joints
    create joints on locators in order clavicle, shoulder, elbow, wrist'''
    def create_arm_locators(self, *args):
        """Function that create locators necessary to for the placement of the arm joints"""
        clavicleLoc = pm.spaceLocator(name='clavicleLoc', p=(0, 0, 0))
        clavicleLoc_group = pm.group(clavicleLoc, n='clavicle_Loc_Grp')
        shoulderLoc = pm.spaceLocator(name='shoulder_Loc', p=(2, 0, -0.5))
        self.nrh_cleanup(shoulderLoc)
        shoulderLoc_group = pm.group(n='shoulder_Loc_Grp')
        parent_shoulderGrp_clavGrp = pm.parent(shoulderLoc_group, clavicleLoc_group)
        elbowLoc = pm.spaceLocator(name='elbow_Loc', p=(5, 0, -1.5))
        self.nrh_cleanup(elbowLoc)
        wristLoc = pm.spaceLocator(name='wrist_Loc', p=(9, 0, -0.5))
        self.nrh_cleanup(wristLoc)

        parent_wrist_shoulderGrp = pm.parent(wristLoc, shoulderLoc_group)
        parent_elbow_shoulderGrp = pm.parent(elbowLoc, shoulderLoc_group)


        pm.ls(selection=False)

        pm.xform(clavicleLoc_group, relative= True, translation=(3.188069, 28.0, 0.0))
        pm.xform(elbowLoc, relative=True, translation=(0, -1.5, 0.0))
        pm.xform(wristLoc, relative=True, translation=(0, -3.0, 0.0))


        '''create a list of variables to grab and replace with joints'''

        global arm_position_locator
        arm_position_locator = (clavicleLoc, shoulderLoc_group, shoulderLoc, elbowLoc, wristLoc)

        '''testing a way to get the value of the check box in the UI'''
        # global locator_created
        # for asymmetrical_checked in locator_created:
        #     if pm.checkBox(asymmetrical_checked,query=True, value=True):
        #         print('You have checked the Asymmetrical option')

        self.checkbox_evalutaion()
        # leftArm_locators = create_arm_locators()
        print('Left arm locators created')

        return arm_position_locator

    '''here is a script i wrote specifically for the module to calculate the correct vectors using maths
    will need to readdress the polevector selection on the right side and leg modules though'''
    def l_nrhCalculateVector(self):
        shoulderJnt = pm.xform('l_shoulder_ik', q=1, ws=1, t=1)
        elbowJnt = pm.xform('l_elbow_ik', q=1, ws=1, t=1)
        wristJnt = pm.xform('l_wrist_ik', q=1, ws=1, t=1)

        shoulder_vector = OpenMaya.MVector(shoulderJnt[0], shoulderJnt[1], shoulderJnt[2])
        elbow_vector = OpenMaya.MVector(elbowJnt[0], elbowJnt[1], elbowJnt[2])
        wrist_vector = OpenMaya.MVector(wristJnt[0], wristJnt[1], wristJnt[2])

        shoulderToWrist = wrist_vector - shoulder_vector
        shoulderToElbow = elbow_vector - shoulder_vector

        dotProduct = shoulderToElbow * shoulderToWrist

        projectionLength = float(dotProduct) / float(shoulderToWrist.length())

        shoulderToWrist_normalize = shoulderToWrist.normal()

        projectionVector = shoulderToWrist_normalize * projectionLength

        arrowVector = shoulderToElbow - projectionVector
        arrowVector *= 5
        finalVector = arrowVector + elbow_vector

        pvControl = 'l_arm_pv_ctrl_grp'

        pm.xform(pvControl, ws=1, t=(finalVector.x, finalVector.y, finalVector.z))

    def r_nrhCalculateVector(self):
        shoulderJnt = pm.xform('r_shoulder_ik', q=1, ws=1, t=1)
        elbowJnt = pm.xform('r_elbow_ik', q=1, ws=1, t=1)
        wristJnt = pm.xform('r_wrist_ik', q=1, ws=1, t=1)

        shoulder_vector = OpenMaya.MVector(shoulderJnt[0], shoulderJnt[1], shoulderJnt[2])
        elbow_vector = OpenMaya.MVector(elbowJnt[0], elbowJnt[1], elbowJnt[2])
        wrist_vector = OpenMaya.MVector(wristJnt[0], wristJnt[1], wristJnt[2])

        shoulderToWrist = wrist_vector - shoulder_vector
        shoulderToElbow = elbow_vector - shoulder_vector

        dotProduct = shoulderToElbow * shoulderToWrist

        projectionLength = float(dotProduct) / float(shoulderToWrist.length())

        shoulderToWrist_normalize = shoulderToWrist.normal()

        projectionVector = shoulderToWrist_normalize * projectionLength

        arrowVector = shoulderToElbow - projectionVector
        arrowVector *= 5
        finalVector = arrowVector + elbow_vector

        pvControl = 'r_arm_pv_ctrl_grp'

        pm.xform(pvControl, ws=1, t=(finalVector.x, finalVector.y, finalVector.z))

    def setSDKs(self):
        '''left side'''
        l_hand_icon = self.create_nrhStar()
        pm.rename(l_hand_icon, 'l_hand_ctrl')

        '''create hand ctrl and switch attr'''
        self.create_hand_attributes(l_hand_icon)

        l_hand_ctrl_offset = pm.group(l_hand_icon, n='l_handCtrl_offset')
        l_trash_parent = pm.parentConstraint('l_wrist_Jnt', 'l_handCtrl_offset', mo=False)
        pm.delete(l_trash_parent)


        pm.move(l_hand_ctrl_offset, 0,2.3,0, r=1, os=1, wd=1)
        pm.parentConstraint('l_wrist_Jnt', l_hand_ctrl_offset, mo=True)
        # pm.xform(l_hand_icon, t=(4.5, 1.5, 0), ro=(13, 0, 0))
        # nrh_cleanup()

        arm_01_contraint = pm.orientConstraint('l_shoulder_ik', 'l_shoulder_fk', 'l_shoulder_Jnt', mo=False)
        arm_02_contraint = pm.orientConstraint('l_elbow_ik', 'l_elbow_fk', 'l_elbow_Jnt', mo=False)

        arm_01_weights = arm_01_contraint.getWeightAliasList()
        arm_01_weights[0].set(1)
        arm_01_weights[1].set(0)

        arm_02_weights = arm_02_contraint.getWeightAliasList()
        arm_02_weights[0].set(1)
        arm_02_weights[1].set(0)

        pm.setDrivenKeyframe(arm_01_weights, currentDriver='l_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_01_weights, currentDriver='l_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='l_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='l_hand_ctrl.ikFk')

        # print('ikfk key 1 is set')
        pm.setAttr('l_hand_ctrl.ikFk', 10)

        arm_01_weights[0].set(0)
        arm_01_weights[1].set(1)

        arm_02_weights[0].set(0)
        arm_02_weights[1].set(1)

        pm.setDrivenKeyframe(arm_01_weights, currentDriver='l_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_01_weights, currentDriver='l_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='l_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='l_hand_ctrl.ikFk')

        # print('ikfk 2nd key is set')

        pm.setAttr("l_hand_ctrl.ikFk", 0)

        pm.setAttr("l_armIK_ctrl.visibility", 1)
        pm.setDrivenKeyframe('l_armIK_ctrl.visibility', currentDriver='l_hand_ctrl.ikFk')
        print('ikfk key 1 is set')

        pm.setAttr("l_hand_ctrl.ikFk", 10)

        pm.setAttr("l_armIK_ctrl.visibility", 0)
        pm.setDrivenKeyframe('l_armIK_ctrl.visibility', currentDriver='l_hand_ctrl.ikFk')
        print('ikfk 2nd key is set')

        pm.setAttr("l_hand_ctrl.ikFk", 0)

        pm.setAttr("l_fk_01_ctrl.visibility", 0)
        pm.setDrivenKeyframe('l_fk_01_ctrl.visibility', currentDriver='l_hand_ctrl.ikFk')
        print('ikfk key 3 is set')

        pm.select('l_fk_01_ctrl', r=1)
        pm.select('l_hand_ctrl', r=1)
        pm.setAttr("l_hand_ctrl.ikFk", 10)
        pm.setAttr("l_fk_01_ctrl.visibility", 1)
        pm.setDrivenKeyframe('l_fk_01_ctrl.visibility', currentDriver='l_hand_ctrl.ikFk')
        print('ikfk key 4 is set')

        pm.setAttr("l_hand_ctrl.ikFk", 0)

        '''right side'''
        r_hand_icon = self.create_nrhStar()
        pm.rename(r_hand_icon, 'r_hand_ctrl')

        '''create hand ctrl and switch attr'''
        self.create_hand_attributes(r_hand_icon)

        r_hand_ctrr_offset = pm.group(r_hand_icon, n='r_handCtrr_offset')
        r_trash_parent = pm.parentConstraint('r_wrist_Jnt', 'r_handCtrr_offset', mo=False)
        pm.delete(r_trash_parent)


        pm.move(r_hand_ctrr_offset, 0,-2.3,0, r=1, os=1, wd=1)
        pm.parentConstraint('r_wrist_Jnt', r_hand_ctrr_offset, mo=True)
        # pm.xform(r_hand_icon, t=(4.5, 1.5, 0), ro=(13, 0, 0))
        # nrh_cleanup()

        arm_01_contraint = pm.orientConstraint('r_shoulder_ik', 'r_shoulder_fk', 'r_shoulder_Jnt', mo=False)
        arm_02_contraint = pm.orientConstraint('r_elbow_ik', 'r_elbow_fk', 'r_elbow_Jnt', mo=False)

        arm_01_weights = arm_01_contraint.getWeightAliasList()
        arm_01_weights[0].set(1)
        arm_01_weights[1].set(0)

        arm_02_weights = arm_02_contraint.getWeightAliasList()
        arm_02_weights[0].set(1)
        arm_02_weights[1].set(0)

        pm.setDrivenKeyframe(arm_01_weights, currentDriver='r_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_01_weights, currentDriver='r_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='r_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='r_hand_ctrl.ikFk')

        # print('ikfk key 1 is set')
        pm.setAttr('r_hand_ctrl.ikFk', 10)

        arm_01_weights[0].set(0)
        arm_01_weights[1].set(1)

        arm_02_weights[0].set(0)
        arm_02_weights[1].set(1)

        pm.setDrivenKeyframe(arm_01_weights, currentDriver='r_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_01_weights, currentDriver='r_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='r_hand_ctrl.ikFk')
        pm.setDrivenKeyframe(arm_02_weights, currentDriver='r_hand_ctrl.ikFk')

        # print('ikfk 2nd key is set')

        pm.setAttr("r_hand_ctrl.ikFk", 0)

        pm.setAttr("r_armIK_ctrl.visibility", 1)
        pm.setDrivenKeyframe('r_armIK_ctrl.visibility', currentDriver='r_hand_ctrl.ikFk')
        print('ikfk key 1 is set')

        pm.setAttr("r_hand_ctrl.ikFk", 10)

        pm.setAttr("r_armIK_ctrl.visibility", 0)
        pm.setDrivenKeyframe('r_armIK_ctrl.visibility', currentDriver='r_hand_ctrl.ikFk')
        print('ikfk 2nd key is set')

        pm.setAttr("r_hand_ctrl.ikFk", 0)

        pm.setAttr("r_fk_01_ctrl.visibility", 0)
        pm.setDrivenKeyframe('r_fk_01_ctrl.visibility', currentDriver='r_hand_ctrl.ikFk')
        print('ikfk key 3 is set')

        pm.select('r_fk_01_ctrl', r=1)
        pm.select('r_hand_ctrl', r=1)
        pm.setAttr("r_hand_ctrl.ikFk", 10)
        pm.setAttr("r_fk_01_ctrl.visibility", 1)
        pm.setDrivenKeyframe('r_fk_01_ctrl.visibility', currentDriver='r_hand_ctrl.ikFk')
        print('ikfk key 4 is set')

        pm.setAttr("r_hand_ctrl.ikFk", 0)

        pm.setAttr("l_shoulder_ik.visibility", 0)
        pm.setAttr("r_shoulder_ik.visibility", 0)

        pm.setAttr("l_shoulder_fk.visibility", 0)
        pm.setAttr("r_shoulder_fk.visibility", 0)

    def create_hand_attributes(self, hand_icon):
        '''hand attributes and switch for IK/FK on the icon'''
        hand_icon.addAttr('Attributes', k=1, at='enum', en='----------:')
        hand_icon.addAttr('ikFk', k=1, min=0, max=10)
        hand_icon.addAttr('Hand', k=1, at='enum', en='----------:')
        hand_icon.addAttr('Fist', k=1, min=-10, max=10)
        hand_icon.addAttr('Spread', k=1, min=-10, max=10)
        hand_icon.addAttr('Fingers', k=1, at='enum', en='-----:')
        hand_icon.addAttr('Index_curl', k=1, min=-10, max=10)
        hand_icon.addAttr('Index_twist', k=1, min=-10, max=10)
        hand_icon.addAttr('Middle_curl', k=1, min=-10, max=10)
        hand_icon.addAttr('Middle_twist', k=1, min=-10, max=10)
        hand_icon.addAttr('Ring_curl', k=1, min=-10, max=10)
        hand_icon.addAttr('Ring_twist', k=1, min=-10, max=10)
        hand_icon.addAttr('Pinky_curl', k=1, min=-10, max=10)
        hand_icon.addAttr('Pinky_twist', k=1, min=-10, max=10)
        hand_icon.addAttr('Thumb', k=1, at='enum', en='-----:')
        hand_icon.addAttr('Thumb_curl', k=1, min=-10, max=10)
        hand_icon.addAttr('Thumb_twist', k=1, min=-10, max=10)
        hand_icon.addAttr('Thumb_spread', k=1, min=-10, max=10)

    def create_nrhStar(self):
        star = pm.circle(name='hand_ctrl', c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, tol=0.01, s=16, ch=1)[
            0]
        print(star)
        pm.xform(star.cv[0::2], s=[3, 3, 3])
        return star



    '''will eventually want to have the locators different colors as to help differentiate sides and which limb
    is being laid out add in modularity so if mesh  is not symmetrical they can pose and replace both sides with
    locators or if symmetrical then the can simple have it build for them automatically'''

    def create_joints_on_locators(self, item):
        print ('Initiate Joint swap')
        position_output = []
        joint_list = []

        '''getting the point position data of the things in the list and pinning their position in space'''
        for i in item:
            items = pm.pointPosition(i, world=True)
            print ('item added to position outputs')
            position_output.append(items)

            print(position_output)

        pm.delete(item)

        '''for the things in position_output create joints based on their location'''
        for j in position_output:
            test_joints = pm.joint(name='', position=j, absolute=True)
            print ('item added to joint list')
            # pm.parent(world=True)
            joint_list.append(test_joints)

        pm.select(cl=True)
        print (item)

        '''takes the 3 joint in the chain (the shoulder in this case) and orients joints and sets secondary axis'''
        # pm.parent(joint_list[2], world=True)
        pm.joint(joint_list[2], e=True, ch=True, oj='xyz')

        '''Set pref angle for the joints'''

        pm.rotate(joint_list[2], 0, -50, 0, r=1, os=1, fo=1)
        pm.joint(joint_list[2], edit=True, children=True, setPreferredAngles=True)
        pm.rotate(joint_list[2], 0, 50, 0, r=1, os=1, fo=1)

        # pm.rotate(joint_list[3], 0, -50, 0, r=1, os=1, fo=1)
        # pm.joint(joint_list[3], edit=True, children=True, setPreferredAngles=True)
        # pm.rotate(joint_list[3], 0, 50, 0, r=1, os=1, fo=1)

        '''create a single chain ik handle for clavicle
        then create 2 more joint chain off the new joints with IK and FK names instead on Jnt
        parent these new joints to the main arm joint system (shoulder, elbow, wrist)'''

        clav_jnt = pm.rename(joint_list[0], 'l_clavicle_Jnt')
        clav_end = pm.rename(joint_list[1], 'l_clavicle_End')
        pm.delete('clavicle_Loc_Grp')
        '''Creates the clavicle IK'''
        clavicle_Ik = pm.ikHandle(sj=joint_list[0], ee=joint_list[1], name='l_clav_IK', sol='ikSCsolver', autoPriority=True)

        '''create the left clavicle ik control'''
        mel.eval("source arrowControl;")
        clavCtrl_group = pm.rename('arrow_ctrl_grp', 'l_clav_ctrl_grp')
        clavCtrl = pm.rename('arrow_ctrl', 'l_clav_ctrl')
        pm.rotate(clavCtrl, 90, 0, 0, r=1, os=1, fo=1)
        cmds.makeIdentity('l_clav_ctrl', apply=True, t=1, r=1, s=1, n=0)
        proxyParent_clav = pm.parentConstraint('l_clavicle_End', clavCtrl_group, mo=False)
        pm.delete(proxyParent_clav)

        l_clavEnd_pivot = pm.xform("l_clavicle_End", q=True, t=True, ws=True)
        cmds.select('l_clav_ctrl_grp', r=1)
        cmds.move(0, 2.31504, 0, r=1, os=1, wd=1)
        cmds.move(l_clavEnd_pivot[0],l_clavEnd_pivot[1],l_clavEnd_pivot[2], 'l_clav_ctrl_grp.scalePivot', 'l_clav_ctrl_grp.rotatePivot', rpr=1, ws=True)
        cmds.select('l_clav_ctrl', r=1)
        cmds.move(0, -2.31504, 0, 'l_clav_ctrl.scalePivot', 'l_clav_ctrl.rotatePivot', r=1)
        pm.select(cl=True)

        pm.parent('l_clav_IK', 'l_clav_ctrl')


        shoulder_jnt = pm.rename(joint_list[2], 'l_shoulder_Jnt')
        elbow_jnt = pm.rename(joint_list[3], 'l_elbow_Jnt')
        wrist_jnt = pm.rename(joint_list[4], 'l_wrist_Jnt')

        ikarm_grp = []
        fkarm_grp = []

        ikshoulder = ikarm_grp.append(pm.duplicate(joint_list[2], parentOnly=True, name='l_shoulder_ik'))
        ikelbow = ikarm_grp.append(pm.duplicate(joint_list[3], parentOnly=True, name='l_elbow_ik'))
        ikwrist = ikarm_grp.append(pm.duplicate(joint_list[4], parentOnly=True, name='l_wrist_ik'))

        pm.parent(ikarm_grp[2], ikarm_grp[1])
        pm.parent(ikarm_grp[1], ikarm_grp[0])

        fkshoulder = fkarm_grp.append(pm.duplicate(joint_list[2], parentOnly=True, name='l_shoulder_fk'))
        fkelbow = fkarm_grp.append(pm.duplicate(joint_list[3], parentOnly=True, name='l_elbow_fk'))
        fkwrist = fkarm_grp.append(pm.duplicate(joint_list[4], parentOnly=True, name='l_wrist_fk'))

        pm.parent(fkarm_grp[2], fkarm_grp[1])
        pm.parent(fkarm_grp[1], fkarm_grp[0])
        pm.parent(joint_list[2], clav_end)

        left_poleVectorCtrl = pm.circle(name='l_arm_pv_Ctrl', c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))
        cvSelection = pm.select('l_arm_pv_Ctrl.cv[2]','l_arm_pv_Ctrl.cv[0]', 'l_arm_pv_Ctrl.cv[6]', 'l_arm_pv_Ctrl.cv[4]')
        cmds.scale(0.0411462, 0.0411462, 0.0411462, ocp=1, r=1)
        pm.select(left_poleVectorCtrl)
        cmds.rotate(90, 0, 0, r=1, os=1, fo=1)
        # freeze objects transforms
        freezeTransforms = cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        # delete object history
        deleteHistory = cmds.delete(constructionHistory=True)

        poleVector_grp = pm.group(name='l_arm_pv_ctrl_grp')

        # freeze objects transforms
        freezeTransforms = cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        # delete object history
        deleteHistory = cmds.delete(constructionHistory=True)
        cmds.xform('l_arm_pv_ctrl_grp', centerPivots=True)
        pm.select(cl=True)

        '''create the controls'''
        mel.eval("source nurbCube;")
        armIk_control = pm.rename('curve1', 'l_armIK_ctrl')
        armIk_control_group = pm.group(armIk_control, name='l_armIK_ctrl_grp')

        pm.setAttr("l_armIK_ctrl_grp.scaleZ", 3)
        pm.setAttr("l_armIK_ctrl_grp.scaleX", 3)
        pm.setAttr("l_armIK_ctrl_grp.scaleY", 3)

        proxyParent_wrist = pm.parentConstraint('l_wrist_Jnt', armIk_control_group, mo=False)
        pm.delete(proxyParent_wrist)

        '''calculate the correct vector'''
        self.l_nrhCalculateVector()

        '''create the arm Ik'''
        l_armIk = pm.ikHandle(sj='l_shoulder_ik', ee='l_wrist_ik', name='l_arm_IK', sol='ikRPsolver',
                                  autoPriority=True)
        pm.parent('l_arm_IK', armIk_control)

        pm.poleVectorConstraint('l_arm_pv_Ctrl', 'l_arm_IK')

        '''create the fk controls and the wrist control with attrs'''
        self.l_nrhautofk()
        pm.select(cl=True)
        pm.rename('group1', 'l_fk_controlOffset_01')
        pm.rename('group2', 'l_fk_controlOffset_02')
        pm.rename('nurbsCircle1', 'l_fk_01_ctrl')
        pm.rename('nurbsCircle2', 'l_fk_02_ctrl')
        pm.parentConstraint('l_clavicle_End', 'l_fk_controlOffset_01', mo=True)

        # '''Will toggle if boxes are checked eventually'''
        # if symetrical checkbox == True, and asymmetrical checkbox == False:
        #     then proceed
        '''create right side joints based off of the left'''
        rightSide_joints = pm.mirrorJoint('l_clavicle_Jnt', mirrorBehavior=1, mirrorYZ=1, searchReplace=("l_", "r_"))

        '''quick cleanup the ik's joints'''
        cmds.setAttr("r_shoulder_ik.rotateX", 0)
        cmds.setAttr("r_shoulder_ik.rotateY", 0)
        cmds.setAttr("r_shoulder_ik.rotateZ", 0)

        cmds.setAttr("r_elbow_ik.rotateX", 0)
        cmds.setAttr("r_elbow_ik.rotateY", 0)
        cmds.setAttr("r_elbow_ik.rotateZ", 0)

        pm.delete('effector3')

        '''creates pole vector ctrl'''
        right_poleVectorCtrl = pm.circle(name='r_arm_pv_Ctrl', c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))
        pm.select('r_arm_pv_Ctrl.cv[2]','r_arm_pv_Ctrl.cv[0]', 'r_arm_pv_Ctrl.cv[6]', 'r_arm_pv_Ctrl.cv[4]')
        cmds.scale(0.0411462, 0.0411462, 0.0411462, ocp=1, r=1)
        pm.select(right_poleVectorCtrl)
        cmds.rotate(-90, 0, 0, r=1, os=1, fo=1)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        cmds.delete(constructionHistory=True)

        r_poleVector_grp = pm.group(name='r_arm_pv_ctrl_grp')

        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        cmds.delete(constructionHistory=True)
        cmds.xform('l_arm_pv_ctrl_grp', centerPivots=True)
        pm.select(cl=True)


        '''create the right clavicle ik control'''
        mel.eval("source arrowControl2;")
        r_clavCtrl_group = pm.rename('arrow_ctrl_grp', 'r_clav_ctrl_grp')
        r_clavCtrl = pm.rename('arrow_ctrl', 'r_clav_ctrl')
        pm.rotate(r_clavCtrl, -90, 0, 0, r=1, os=1, fo=1)
        cmds.makeIdentity('r_clav_ctrl', apply=True, t=1, r=1, s=1, n=0)
        r_proxyParent_clav = pm.parentConstraint('r_clavicle_End', r_clavCtrl_group, mo=False)
        pm.delete(r_proxyParent_clav)

        r_clavEnd_pivot = pm.xform("r_clavicle_End", q=True, t=True, ws=True)
        cmds.select('r_clav_ctrl_grp', r=1)
        cmds.move(0, -2.31504, 0, r=1, os=1, wd=1)
        cmds.move(-5.188069, 28, -0.5, 'r_clav_ctrl_grp.scalePivot', 'r_clav_ctrl_grp.rotatePivot', rpr=1)
        cmds.select('r_clav_ctrl', r=1)
        cmds.move(r_clavEnd_pivot[0],r_clavEnd_pivot[1],r_clavEnd_pivot[2], 'r_clav_ctrl_grp.scalePivot', 'r_clav_ctrl_grp.rotatePivot', rpr=1, ws=True)
        pm.select(cl=True)

        pm.parent('r_clav_IK', 'r_clav_ctrl')

        '''create ik system on right side'''
        '''create the controls'''
        mel.eval("source nurbCube;")
        r_armIk_control = pm.rename('curve1', 'r_armIK_ctrl')
        r_armIk_control_group = pm.group(r_armIk_control, name='r_armIK_ctrl_grp')

        pm.setAttr("r_armIK_ctrl_grp.scaleZ", 3)
        pm.setAttr("r_armIK_ctrl_grp.scaleX", 3)
        pm.setAttr("r_armIK_ctrl_grp.scaleY", 3)

        r_proxyParent_wrist = pm.parentConstraint('r_wrist_Jnt', r_armIk_control_group, mo=False)
        pm.delete(r_proxyParent_wrist)

        '''calculate the correct vector, right side'''
        self.r_nrhCalculateVector()

        '''create the arm Ik'''
        r_armIk = pm.ikHandle(sj='r_shoulder_ik', ee='r_wrist_ik', name='r_arm_IK', sol='ikRPsolver',
                                  autoPriority=True)
        pm.parent('r_arm_IK', r_armIk_control)

        pm.poleVectorConstraint('r_arm_pv_Ctrl', 'r_arm_IK')

        '''create the right fk system'''
        self.r_nrhautofk()
        pm.select(cl=True)
        pm.rename('group1', 'r_fk_controlOffset_01')
        pm.rename('group2', 'r_fk_controlOffset_02')
        pm.rename('nurbsCircle1', 'r_fk_01_ctrl')
        pm.rename('nurbsCircle2', 'r_fk_02_ctrl')
        pm.parentConstraint('r_clavicle_End', 'r_fk_controlOffset_01', mo=True)
        pm.delete('group3')

        '''setup the set driven key for ikfk switch and control visibility'''
        self.setSDKs()

        return (joint_list, ikarm_grp, fkarm_grp)

    def ikfk_setup(self):
        pass



run_arm_class = armRig()

'''source: nurbCube.mel, arrowControl.mel, arrowControl2.mel, nrhArmAutorigv004.py'''
