# ik/fk arm auto rig v002
# Nate Hancock
# created 6/14/2022

import maya.cmds as cmds
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
    # clean up an object
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
        count = 1

        # create locators
        clavicleLoc = pm.spaceLocator(name='clavicle_Loc', p=(0, 0, 0))
        self.nrh_cleanup(clavicleLoc)
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
        # parent_shoulder_shoulderGrp = pm.parent(shoulderLoc, shoulderLoc_group)
        # parent_shoulderGrp_clavGrp = pm.parent(shoulderLoc_group, clavicleLoc_group)

        pm.ls(selection=False)

        pm.xform(clavicleLoc_group, relative= True, translation=(3.188069, 28.0, 0.0))
        pm.xform(elbowLoc, relative=True, translation=(0, -1.5, 0.0))
        pm.xform(wristLoc, relative=True, translation=(0, -3.0, 0.0))
        # pm.xform(shoulderLoc_group, relative= True, rotation=(0.0, 0.0, -35.0))

        # nrhCleanup(clavicleLoc_group)

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

    '''will eventually want to have the locators different colors as to help differentiate sides and which limb
    is being laid out add in modularity so if mesh  is not symmetrical they can pose and replace both sides with
    locators or if symmetrical then the can simple have it build for them automatically'''

    '''replace locators with joint chain'''
    # def create_arm_joints(items, *args):
    #     #model function for replacement
    #     '''test_locator = pm.spaceLocator(name= 'Test 01')
    #     pm.xform(test_locator, t = (2, 5, 0))
    #     pm.select(cl= True)
    #
    #     position_output = pm.pointPosition(test_locator)
    #
    #     print (position_output)
    #
    #     test_joint = pm.joint(name = 'Test Jnt', position = position_output)
    #
    #     pm.delete (test_locator)'''
    #
    #     count = 1
    #     for locators in items:
    #         position_output = pm.pointPosition(items)
    #
    #         print(position_output)
    #
    #         test_joint = pm.joint(name='Test Jnt', position=position_output)
    #
    #         pm.delete(test_locator)

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
            joint_list.append(test_joints)

            # '''will need to rename arm joints in series (joints : 'clav', 'clav end', 'shoulder', 'elbow', 'arm end')'''
            # '''May move this to a seperate function altogether, especially since loop causes count issue'''
            # count = 0
            # name = 'arm'
            # suffix = 'Jnt'
            # prefix = 'L'
            #
            # for names in test_joints:
            #     # print(test_joints)
            #     new_name = '{0}_{1}_{2}_{3}'.format(prefix, name, suffix, count)
            #     pm.rename(test_joints, new_name)
            #     count += 1

        pm.select(cl=True)

        # '''need to find a way to maintain forward and up vector when orienting joints to x check axis kwargs'''
        # for k in joint_list:
        #     # pm.joint(joint_list, zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
        #     pm.rotate(joint_list, 0, -45, 0, r=1, os=1, fo=1)
        #     pm.joint(joint_list, spa=1, ch=1, e=1)
        #     pm.rotate(joint_list, 0, 45, 0, r=1, os=1, fo=1)
        #     pm.joint(joint_list[2], e=True, ch=True, oj='xyz')

        '''takes the 3 joint in the chain (the shoulder in this case) and orients joints and sets secondary axis'''
        pm.parent(joint_list[2], world=True)
        pm.joint(joint_list[2], e=True, ch=True, oj='xyz', secondaryAxisOrient='yup')

        '''Set pref angle for the joints'''

        # pm.rotate(joint_list[2], 0, -45, 0, r=1, os=1, fo=1)
        # pm.joint(joint_list[2], edit=True, children=True, setPreferredAngles=True)
        # pm.rotate(joint_list[2], 0, 45, 0, r=1, os=1, fo=1)
        #
        #
        # pm.rotate(joint_list[3], 0, -45, 0, r=1, os=1, fo=1)
        # pm.joint(joint_list[3], edit=True, children=True, setPreferredAngles=True)
        # pm.rotate(joint_list[3], 0, 45, 0, r=1, os=1, fo=1)

        '''create a single chain ik handle for clavicle
        then create 2 more joint chain off the new joints with IK and FK names instead on Jnt
        parent these new joints to the main arm joint system (shoulder, elbow, wrist)'''

        print (item)

        '''Icky shameful code need to cleanup'''
        pm.delete('clavicle_Loc_Grp')

        clav_jnt = pm.rename(joint_list[0], 'L_clavicle_Jnt')
        clav_end = pm.rename(joint_list[1], 'L_clavicle_End')
        clavicle_Ik = pm.ikHandle(sj=joint_list[0], ee=joint_list[1], name='clav_IK', sol='ikSCsolver', autoPriority=True)

        shoulder_jnt = pm.rename(joint_list[2], 'L_shoulder_Jnt')
        elbow_jnt = pm.rename(joint_list[3], 'L_elbow_Jnt')
        wrist_jnt = pm.rename(joint_list[4], 'L_wrist_Jnt')

        ikarm_grp = []
        fkarm_grp = []

        clavJnt_grp = pm.group(joint_list[0], name='Clav_Jnt_Grp')
        shoulderJnt_grp = pm.group(joint_list[2], name='Arm_Joints_Grp')

        ikshoulder = ikarm_grp.append(pm.duplicate(joint_list[2], parentOnly=True, name='shoulder_ik'))
        ikelbow = ikarm_grp.append(pm.duplicate(joint_list[3], parentOnly=True, name='elbow_ik'))
        ikwrist = ikarm_grp.append(pm.duplicate(joint_list[4], parentOnly=True, name='wrist_ik'))

        pm.parent(ikarm_grp[2], ikarm_grp[1])
        pm.parent(ikarm_grp[1], ikarm_grp[0])

        fkshoulder = fkarm_grp.append(pm.duplicate(joint_list[2], parentOnly=True, name='shoulder_fk'))
        fkelbow = fkarm_grp.append(pm.duplicate(joint_list[3], parentOnly=True, name='elbow_fk'))
        fkwrist = fkarm_grp.append(pm.duplicate(joint_list[4], parentOnly=True, name='wrist_fk'))

        pm.parent(fkarm_grp[2], fkarm_grp[1])
        pm.parent(fkarm_grp[1], fkarm_grp[0])
        pm.parent(shoulderJnt_grp, clav_end)

        '''create the Ik'''
        l_armIk = pm.ikHandle(sj='shoulder_ik', ee='wrist_ik', name='L_arm_IK', sol='ikRPsolver',
                                  autoPriority=True)

        left_poleVectorCtrl = pm.circle(name='l_arm_pv_Ctrl', c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))
        cvSelection = ('l_arm_pv_Ctrl.cv[2]','l_arm_pv_Ctrl.cv[0]', 'l_arm_pv_Ctrl.cv[6]', 'l_arm_pv_Ctrl.cv[4]')
        pm.select(cvSelection)
        cmds.scale(0.0411462, 0.0411462, 0.0411462, ocp=1, r=1)
        pm.select(left_poleVectorCtrl)
        cmds.rotate(90, 0, 0, r=1, os=1, fo=1)
        # freeze objects transforms
        freezeTransforms = cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        # delete object history
        deleteHistory = cmds.delete(constructionHistory=True)

        created_grp = pm.group(name='l_arm_pv_ctrl_grp')
        proxy_constraint = pm.parentConstraint('elbow_ik', 'l_arm_pv_Ctrl', mo=False)
        pm.delete(proxy_constraint)
        pm.xform(t=(0,0,-10))

        # freeze objects transforms
        freezeTransforms = cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        # delete object history
        deleteHistory = cmds.delete(constructionHistory=True)
        cmds.xform('l_arm_pv_ctrl_grp', centerPivots=True)
        pm.select(cl=True)

        pm.poleVectorConstraint('l_arm_pv_Ctrl', 'L_arm_IK')


        return (joint_list, ikarm_grp, fkarm_grp)


    '''create controls for ik and fk rigs respectively
    make sure it is scalable
    make sure IK is not flipping and has pole vector add in reverse node and attributes for toggle
    make sure rig has stretch and attributes hide stuff correctly and swap correctly'''

    # pose test

run_arm_class = armRig()


# '''reference functions'''
# def rename_joints(joint_chain, ori, name, suffix):
#     count = 1
#     for current_chain in joint_chain:
#         new_name = '{0}_{1}_{2}_{3}'.format(ori, name, count, suffix)
#         current_chain.rename(new_name)
#
#         count += 1
#
#     #this is a function for creating the FK controls
#
# def nrhAutoRig():
#     joint_chain = pm.ls(sl=True, dag=True)
#     last_icon = None
#     control_icons = []
#     for current_joint in joint_chain[0:-1]:
#         print (current_joint)
#         current_icon = pm.circle(radius=4, normal=[1, 0, 0])[0]
#         local_pad = pm.group(n='fkCtrl_offset')
#         waste_icon = pm.parentConstraint(current_joint, local_pad)
#         pm.delete(waste_icon)
#
#         if last_icon:
#             pm.parent(local_pad, last_icon)
#
#         #connect the control back to the joint
#         pm.orientConstraint(current_icon, current_joint)
#
#         last_icon = current_icon
#
#         control_icons.append(current_icon)
#
#     pm.select(control_icons, r=True)


'''later use for this script could be modular so I can create any number of locators and then use it to place 
a joint chain with multiple lengths and still have a functioning rig system'''
