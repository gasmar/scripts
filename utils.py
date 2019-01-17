'''Auto Rotation for wheels of any size.'''
from maya import cmds
from maya import mel



def demmet():
    '''A programming story...'''


def snap(*args):
    '''Snap target to destination.'''
    cmds.delete(cmds.parentConstraint(*args))

    
def description():
    '''Get descriptionription by removing prefixes or suffixes.'''
    sel = cmds.ls(selection=True)

    for each in sel:
        name = each.split('_')
        
        if name[0] == 'ANIM':
            description = name[2]
        elif name[0] == 'c' or name[0] == 'l' or name[0] == 'r':
            description = name[1]    
        else:
            description = name[0]

        # returns selected object(s)' description string
        return str(description)


def side():
    '''Find the object side (if there is one).'''
    sel = cmds.ls(selection=True)

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


def attrLockAndHide(sel):
    cmds.setAttr(sel+'.tx', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.ty', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.tz', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.ry', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.rz', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.sx', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.sy', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.sz', lock=True, keyable=False, channelBox=False)
    cmds.setAttr(sel+'.v', lock=True, keyable=False, channelBox=False)


# def attrLockAndHide(sel, exceptions):
#     sel = cmds.ls(selection=True)
    
#     for each in sel:
#         attrs = cmds.listAttr(each, keyable=True)
        
#         if exceptions == 'all':
#             for attr in attrs:
#                 channel = '%s.%s' % (each, attr)
#                 cmds.setAttr(channel, lock=True, keyable=False, channelBox=False)

#                 return 'DONE'
