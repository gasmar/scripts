from maya import cmds
from maya import mel
import utils.ar_utils as utils
reload(utils)


def base(sel):
    '''Create base locators to measure wheel.'''
    if len(sel) < 1:
        cmds.warning('Please select wheel(s).')
        return
        
    name = '%s_%s' % (utils.side(sel), utils.description(sel))
    wheel = sel
    # create group with locators and their respective distances
    dist1_locator, dist2_locator, center_locator, dist1, dist2, distance_grp = baseLocators(sel)
    # create measure distance node and get diameter
    diameter = measureWheelDistance(sel, dist1, dist2)
    # position the locators based on the wheel's bounding box
    utils.placeLocators(sel, center_locator, dist1_locator, dist2_locator)
    cmds.parent(diameter, distance_grp)

    global base_info
    base_info = dist1_locator, dist2_locator, center_locator, dist1, dist2, diameter, distance_grp, wheel


def autoRotate(sel):
    '''Create auto rotation based on diameter from base locators.'''
    if len(sel) < 1:
        cmds.warning('Please select wheel(s).')
        return

    wheel = base_info[-1]
    dist1_locator = base_info[0]
    dist2_locator = base_info[1]
    center_locator = base_info[2]
    distance_grp = base_info[-2]
    distance = base_info[-3]

    cmds.select(wheel)
    name = '%s_%s' % (utils.side(sel), utils.description(sel))
    # create group that holds autoRotate connections
    auto_rotate_grp = autoRotateGrp(sel)
    cmds.addAttr(auto_rotate_grp, longName='offset', attributeType='double', defaultValue=0)
    cmds.setAttr('%s.%s' % (auto_rotate_grp, 'offset'), keyable=True)

    # create control to drive autoRotate grp
    auto_rotate_ctrl = autoRotateCtrl(center_locator, sel)
    cmds.addAttr(auto_rotate_ctrl, longName='auto', attributeType='bool', defaultValue=1)
    cmds.setAttr('%s.%s' % (auto_rotate_ctrl[0], 'auto'), keyable=True)
    cmds.makeIdentity(auto_rotate_ctrl, apply=True)

    # create group that drives the autoRotate group's orientation
    orient_grp = cmds.group(auto_rotate_grp, name=name+'_orient_GRP', relative=True)
    cmds.orientConstraint(auto_rotate_ctrl, orient_grp, maintainOffset=True)

    offset_ctrl = offsetCtrl(auto_rotate_ctrl, sel)
    cmds.parent(center_locator, auto_rotate_ctrl[0])
    cmds.makeIdentity(offset_ctrl, apply=True)
    cmds.xform(offset_ctrl, centerPivots=True)
    utils.attrLockAndHide(offset_ctrl, 'tx ty tz ry rz sx sy sz v')

    # expression that drives autoRotate group's rotateX and offset attribute
    wheelExpression(auto_rotate_grp+'.rotateX', auto_rotate_ctrl[0], auto_rotate_grp, distance, wheel)

    center_locator_constraint = cmds.ls(center_locator, dagObjects=True)[-1]
    cmds.delete(center_locator_constraint)

    cmds.pointConstraint(center_locator, auto_rotate_grp)
    cmds.scaleConstraint(center_locator, auto_rotate_grp)

    cmds.parent(distance, auto_rotate_ctrl[0])
    cmds.parent(dist1_locator, dist2_locator, wheel)

    cmds.parent(wheel, offset_ctrl[0])
    cmds.parent(offset_ctrl[0], auto_rotate_grp)

    # cleanup
    cmds.delete(distance_grp)
    cmds.select(clear=True)


def baseLocators(sel):
    '''Locators for wheel measurements.'''
    name = '%s_%s' % (utils.side(sel), utils.description(sel))

    dist1_locator = utils.createLocator(name+'_wheelDist01_LOC', 0, 0, 0)
    dist2_locator = utils.createLocator(name+'_wheelDist02_LOC', 0, 0, 0)
    center_locator = utils.createLocator(name+'_wheelCenter_LOC', 0, 0, 0)
    distance_grp = cmds.group(center_locator, dist1_locator, dist2_locator, name=name+'_locs_GRP')

    cmds.move(0, 0, 1, dist1_locator)
    cmds.move(0, 0, -1, dist2_locator)

    cmds.parentConstraint(dist1_locator, dist2_locator, center_locator)
    cmds.select(clear=True)

    dist1 = cmds.xform(dist1_locator, query=True, translation=True)
    dist2 = cmds.xform(dist2_locator, query=True, translation=True)

    # returns points in space (as locators) to be used in measureWheelDistance()
    return (dist1_locator, dist2_locator, center_locator, dist1, dist2, distance_grp)


def measureWheelDistance(sel, dist1, dist2):
    '''Distance node to find wheel diameter.'''
    name = '%s_%s_DIST' % (utils.side(sel), utils.description(sel))

    distance = cmds.distanceDimension(startPoint=dist1, endPoint=dist2)
    distance = cmds.rename('distanceDimension1', name)

    # returns dynamic distance node, driven by baseLocators()
    return distance
        

def autoRotateGrp(sel):
    '''Group node that contains autoRotate expression and constraints.'''
    name = '%s_%s_%s' % (utils.side(sel), utils.description(sel), 'autoRotate_GRP')

    wheel = base_info[-1]
    grp = cmds.group(wheel, name=name)

    cmds.xform(grp, centerPivots=True)

    # returns group to be driven by connections to achieve automatic rotation
    return grp


def autoRotateCtrl(locator, sel):
    name = '%s_%s_%s' % (utils.side(sel), utils.description(sel), 'autoRotate_CTRL')

    auto_rotate_ctrl = cmds.circle(name=name)
    cmds.delete(cmds.parentConstraint(locator, auto_rotate_ctrl))

    inputs = cmds.listHistory(auto_rotate_ctrl)
    normal_x = str('%s.normalX') % (inputs[1])
    cmds.setAttr(normal_x, 90)

    # returns ctrl that drives the autoRotate grp
    return auto_rotate_ctrl


def offsetCtrl(auto_rotate_ctrl, sel):
    name = '%s_%s_%s' % (utils.side(sel), utils.description(sel), 'offset_CTRL')

    offset_ctrl = cmds.circle(name=name)
    inputs = cmds.listHistory(offset_ctrl)
    wheel_radius = '%s.radius' % (inputs[1])
    normal_x = '%s.normalX' % (inputs[1])
    center_x = '%s.centerX' % (inputs[1])

    utils.snap(auto_rotate_ctrl, offset_ctrl)

    cmds.setAttr(wheel_radius, 0.6)
    cmds.setAttr(normal_x, 90)
    cmds.setAttr(center_x, 1)

    # returns control that allows for offset, evaluated after initial rotation
    return offset_ctrl


def wheelOrientGrp(sel):
    '''Group node that controls proper rotation of auto wheel rot grp.'''
    name = '%s_%s_%s' % (utils.side(sel), utils.description(sel), '_arOrient_GRP')

    grp = cmds.group(name=name)

    # returns group that will control the rotations Y and Z of autoRotate grp
    return grp


def wheelExpression(target, auto, offset, dist, sel):
    '''Math that controls how the wheel will procedurally rotate.'''
    name = '%s_%s_%s' % (utils.side(sel), utils.description(sel), '_autoRotate_EXP')

    string = '''
                if (%s.auto == 1 ) {
                    $diff = %s.translateZ - %s.offset ;
                    %s.rotateX -= $diff * -360 / (%s.distance*3.14); 
                }; 
                %s.offset = %s.translateZ ;

                ''' % (auto, offset, offset, offset, dist, offset, offset)

    expression = cmds.expression(name=name, object=target, string=string, alwaysEvaluate=True)

    # returns expression with math to achieve automatic rotation based on diameter
    return expression