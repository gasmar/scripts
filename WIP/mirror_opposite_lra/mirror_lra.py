from maya import cmds
from mirror_opposite_lra.utils import mlra_utils as utils
reload(utils)


def mirrorLRA(targets):
    '''Mirror Local Rotation Axis of the opposite of the given target.
       This makes for behaviour that is, by default, not possible without
       some form of altered parenting.'''
    for target in targets:
        opposite_ctrl = checkForOppositeCtrl(target)
        lra_grp = createMirrorGroup(opposite_ctrl)
        
        scaleLRAgrp(lra_grp, opposite_ctrl)
        cmds.select(clear=True)
    
    
    
'''--- Utils specific to transferBlendShapesByUV. ---'''
    
    

def checkForOppositeCtrl(target_ctrl):
    '''Verify if there is an opposite control to the given arg.'''
    side = utils.side(target_ctrl)
    opposite_side = utils.oppositeSide(target_ctrl)
    
    if side and opposite_side:
        opposite_ctrl = target_ctrl.replace(side, opposite_side)
        if cmds.objExists(opposite_ctrl):
            cmds.select(opposite_ctrl)
            
            # if it exists, returns the opposite control
            return opposite_ctrl
        else:
            # if it doesn't exist, it returns a warning.
            return cmds.warning('No opposite control found.')        
                

def createMirrorGroup(opposite_ctrl):
    '''Created a group that serves as the container to alter the Local Rotation Axis.'''
    mirror_lra_grp = cmds.group(opposite_ctrl, 
                                name='{}_mirrorLRA_GRP'.format(opposite_ctrl))
    cmds.xform(mirror_lra_grp, centerPivots=True)
    
    # returns the group node to be altered
    return mirror_lra_grp
    
    
def scaleLRAgrp(lra_grp, opposite_ctrl):
    '''Scales the group inversely with the purpose of flipping the Local Rotation Axis'''
    constraint = cmds.listConnections(opposite_ctrl, type='constraint')
    
    if constraint:
        constrained_object = utils.extractChildFromConstraintName(constraint[0])
        cmds.delete(constraint)
    
    for axis in 'XYZ':
        cmds.setAttr('{}.scale{}'.format(lra_grp, axis), -1)
        
    cmds.setAttr('{}.rotateZ'.format(lra_grp), 180)
        
    if constraint:
        cmds.parentConstraint(opposite_ctrl, constrained_object, 
                              name=constraint[0], maintainOffset=True)
    
    return