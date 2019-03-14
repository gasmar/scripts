'''Transfer Blendshapes by UV utils.'''
from maya import cmds


def getCurrentUV(trg):
    '''Get target uv set.'''
    current_uv = cmds.getAttr('{}.currentUVSet'.format(trg))
    
    #returns the current uv set
    return current_uv


def getBlendShapeNode(trg):
    '''Get object blendshape input.'''
    target_blendshape_nodes = []
    input_connections = cmds.listHistory(trg, pruneDagObjects=True, historyAttr=False)

    for input_cnn in input_connections:
        if cmds.nodeType(input_cnn) == 'blendShape':
            target_blendshape_nodes.append(input_cnn)
    
    # returns a list of blendshape input nodes on target
    return target_blendshape_nodes
    

def getBlendShapesFromNodes(trg, blendshape_nodes):
    '''Get blendshapes in blendshape node.'''
    blendshapes = []
    
    for node in range(len(blendshape_nodes)):
        
        connections = cmds.listConnections(blendshape_nodes[node])
        for cnn in connections:
            if cmds.nodeType(cnn) == 'transform':
                blendshape = '{}.{}'.format(blendshape_nodes[node], cnn)
                if str(cnn) == trg:
                    pass
                else: 
                    blendshapes.append(blendshape)
                    
    # returns a list of blendshapes on each node from the given list
    return blendshapes