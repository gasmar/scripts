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


def attrLockAndHide(sel, exceptions):
    '''Lock and hide attributes based on user input, separated by spaces.'''
    for each in sel:
        attrs = cmds.listAttr(each, keyable=True) 
        
        if exceptions == 'all':
            print exceptions
            for attr in attrs:
                channel = '%s.%s' % (each, attr)
                cmds.setAttr(channel, lock=True, keyable=False, channelBox=False)
                
        elif exceptions != 'all':
            transforms = exceptions.split(' ')
            
            for attr in range(len(transforms)):
                try:
                    
                    channel = '%s.%s' % (each, transforms[attr])
                    cmds.setAttr(channel, lock=True, keyable=False, channelBox=False)
                    print 'LOCKED: ', channel
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
