'''Mirror and manipulate Local Rotation Axis utils.'''
from maya import cmds


def getLRA(target):
    pass
   
# might use for optimization later; not fit for rigBuilder
'''
def side(target):
    world_position = cmds.objectCenter(x=True, y=True, z=True)
    
    if world_position > 0:
        side = 'left'
    elif world_position < 0:
        side = 'right'
    else:
        side = 'none'
    return side
'''
    
def side(target):
    '''Get side based on rigBuilder naming convention.'''
    side = ''
    
    if '_l_' in target:
        side = '_l_'
    elif '_r_' in target:
        side = '_r_'
    elif '_c_' in target:
        side = '_c_'
        cmds.warning('{} is a center control.'.format(target))
    
    # returns a string representing the side of the selected object
    return side
    

def oppositeSide(target):
    '''Finds the opposite side based on the side given.'''
    initial_side = side(target)
    
    if initial_side == '_l_':
        return '_r_'
    elif initial_side == '_r_':
        # returns a string of the opposite side based on the naming convention
        return '_l_'
    else:
        # if opposite sided object doesn't exist:
        return cmds.warning('Could not find opposite side of {}'.format(target))
        
        
def checkConstraintType(constraint):
    '''Verifies what kind of constraint the arg is.'''
    constraint_type = cmds.nodeType(constraint)
    
    # returns a string of the type of constrain. 
    # can be used to create a particular type of constraint
    return constraint_type
    
    
def extractChildFromConstraintName(constraint):
    '''Extracts the name of the object constrained by the given arg.'''
    constraint_type = checkConstraintType(constraint)
    name_segments = constraint.split('_')

    for segment in name_segments:
        if str(constraint_type) in segment:
            name_segments.remove(segment)
    
    constrained_object = '_'.join(name_segments)
    
    # returns the object affected by the given constraint
    return constrained_object