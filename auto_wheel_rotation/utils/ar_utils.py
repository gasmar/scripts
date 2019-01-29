'''Auto Rotation for wheels of any size.'''
from maya import cmds
from maya import mel



def demmet():
    '''A programming story...'''
    print 'AI BI WERKIN!!!'


def selection():
    '''Get selection names.'''
    sel = cmds.ls(selection=True)
    selList = []

    if sel:
        for each in sel:
            selList.append(each)

        items = ' '.join(selList)
        return items
    else:
        cmds.warning('NOTHING! NOTHING I TELL YOU!')
        return False


def snap(*args):
    '''Snap target to destination.'''
    cmds.delete(cmds.parentConstraint(*args))


def checkParent(sel):
    parent = cmds.listRelatives(parent=True)
    
    if not parent:
        new_parent_name = '%s_%s_%s' % (side(sel), description(sel), 'WHEEL_GRP')
        # group_geo = cmds.group(sel, name=name)
        # return group_geo
        return new_parent_name
    else:
        # return parent
        return True


def checkForExistingAutoRotate(sel):
    locator = '%s_%s_autoRotate_EXP' % (side(sel), description(sel))
    print locator
    if cmds.objExists(locator):
        return True
    else:
        return False


def description(sel):
    '''Get descriptionription by removing prefixes or suffixes.'''
    name = sel.split('_')
    for each in sel:
        
        if name[0] == 'ANIM':
            description = name[2]
        elif name[0] == 'c' or name[0] == 'l' or name[0] == 'r':
            description = name[1]    
        else:
            description = name[0]

        # returns selected object(s)' description string
        return str(description)


def side(sel):
    '''Find the object side (if there is one).'''
    for each in sel:
        name = each.split('_')

        if name[0] == 'ANIM':
            side = name[1]
        elif name[0] == 'c' or name[0] == 'l' or name[0] == 'r':
            side = name[0]
        else:
            side = ''

        # returns selected object(s)' side string
        return str(side)


def createLocator(name, x, y, z):
    '''Create a locator in the desired starter position and name.'''
    loc = cmds.spaceLocator(position=(x, y, z), name=name)

    # returns a locator based on parameters
    return loc 
    
    
def placeLocators(obj, center_loc, dist1_loc, dist2_loc):
    '''Place locators based on bounding box of an object.'''
    bottom_tx, bottom_ty, bottom_tz, top_tx, top_ty, top_tz = cmds.exactWorldBoundingBox(obj)

    middle_tx = (bottom_tx + top_tx) / 2
    middle_ty = (bottom_ty + top_ty) / 2
    middle_tz = (bottom_tz + top_tz) / 2

    # center loc
    cmds.xform(center_loc, t=[middle_tx, middle_ty, middle_tz])
    # front center loc
    cmds.xform(dist1_loc, t=[middle_tx, middle_ty, top_tz])
    # back center loc
    cmds.xform(dist2_loc, t=[middle_tx, middle_ty, bottom_tz])
    
    # returns locator translations
    return middle_tx, middle_ty, middle_tz


def attrLockAndHide(sel, exceptions):
    '''Lock and hide attributes based on user input, separated by spaces.'''
    for each in sel:
        attrs = cmds.listAttr(each, keyable=True) 
        
        if exceptions == 'all':
            for attr in attrs:
                channel = '%s.%s' % (each, attr)
                cmds.setAttr(channel, lock=True, keyable=False, channelBox=False)
                
        elif exceptions != 'all':
            transforms = exceptions.split(' ')
            
            for attr in range(len(transforms)):
                try:
                    channel = '%s.%s' % (each, transforms[attr])
                    cmds.setAttr(channel, lock=True, keyable=False, channelBox=False)
                except:
                    print channel, ' doesn\'t exist.'

    return channel


def getInputs(sel):
    '''Get object input attributes.'''
    if len(sel) > 1:
        cmds.confirmDialog(
                           title='Too many objects.', 
                           message='Inputs can only be listed for one object at a time.'
                           )
        cmds.error('Inputs can only be listed for one object at a time.')
        
    for each in range(len(sel)):
        each = sel[each]
        input_attrs = []
        
        try:
            inputs = cmds.listHistory(each, pruneDagObjects=True, historyAttr=False)
            attrs = cmds.listAttr(inputs)
            
            for input in inputs:
                print 'INPUT: ', input
                
                for attr in attrs:
                    print '  -- %s.%s' % (input, attr)
                    
                    input_attrs.append('%s.%s' % (input, attr))
                
        except:
            print 'No inputs on -- %s --' % (each)
            
    # returns a list with every input attribute
    return input_attrs
    
def undo(func):
    '''Chunk undo function for long processes.'''
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return ret
    return wrapper