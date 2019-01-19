from maya import cmds
from maya import mel

def getDeformers(sel):
    '''Finds deformer node (if there is one).'''
    hist = cmds.listHistory(sel)
    deformers = []

    for each in hist:
        types = cmds.nodeType(each)
        if 'deform' in types:
            deformers.append(types)
            cmds.select(each)
    
    # returns deformer nodes, if any
    print deformers
    return deformers

def getMembershipVerts(sel):
    '''Gets verts affected by deformer and activates Edit Membership Tool.'''
    print 'SEL: ', sel[0]
    for each in range(len(sel)):
        print sel[each]
    
    sel_sets = cmds.listSets(extendToShape=True, object=sel[0], type=2)
    
    for each in range(len(sel_sets)):
        type = cmds.nodeType(sel_sets[each])
        
    cmds.select(sel_sets[0], replace=True)
    verts = cmds.ls(selection=True, flatten=True)
    
    for vert in range(len(verts)):
        print verts[vert]
    
    inputs = cmds.listHistory(sel, pruneDagObjects=True, historyAttr=False)
    getDeformers(sel)
    cmds.EditMembershipTool()
    
    # returns deformer-influenced verts
    return verts