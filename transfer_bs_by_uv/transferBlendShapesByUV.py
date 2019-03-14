from maya import cmds
from transfer_bs_by_uv.utils import bsuv_utils as utils
reload(utils)



def transferBlendShapesByUV():
    '''Execute full script.'''
    targets = cmds.ls(sl=True)
    if len(targets) != 2:
        return cmds.error('Please select ONE target and ONE destination.')
        
    default_blendshape = targets[0]
    target_mesh = targets[1]

        
    target_mesh_final = makeCopies(default_blendshape, target_mesh)
    new_blendshapes = makeNewBlendshapes(default_blendshape, target_mesh_final)
        
    # returns group with new blendshapes
    return new_blendshapes


def makeCopies(default_blendshape, target_mesh):
    
    target_mesh_copy = cmds.duplicate(target_mesh, n='{}_COPY'.format(target_mesh), 
                                      returnRootsOnly=True)
                                          
    cmds.transferAttributes(default_blendshape, target_mesh,
                            transferPositions=1,
                            transferNormals=0,
                            transferUVs=2,
                            transferColors=2,
                            sampleSpace=3,
                            sourceUvSpace=utils.getCurrentUV(default_blendshape),
                            targetUvSpace=utils.getCurrentUV(target_mesh),
                            searchMethod=3,
                            flipUVs=0,
                            colorBorders=1)
                            
    target_mesh_final = cmds.duplicate(target_mesh, n='{}_FINAL'.format(target_mesh), 
                                      returnRootsOnly=True)
                                      
    create_blendshape = cmds.blendShape(target_mesh, target_mesh_copy, target_mesh_final, 
                    automatic=True, name='{}_BS'.format(default_blendshape))

    cmds.blendShape('{}.{}'.format(create_blendshape[0], 
                    target_mesh), edit=True, 
                    w=[(0, 1.0), (1, 1.0)])
                    
    cmds.delete(target_mesh_copy)
    
    # returns the mesh that will serve as a dummy to create new duplicates from
    return target_mesh_final


'''--- Utils specific to transferBlendShapesByUV. ---'''



def makeNewBlendshapes(default_blendshape, target_mesh_final):
    '''Make a new, clean piece of geometry from new mesh for every blendshape on old geometry.'''
    blendshape_nodes = utils.getBlendShapeNode(default_blendshape)
    blendshapes = utils.getBlendShapesFromNodes(default_blendshape, blendshape_nodes)
    
    new_bs_group = cmds.group(empty=True, name='BlendShape_GRP')
    
    for current_bs in blendshapes:
        name = newBlendShapeNames(current_bs)

        cmds.setAttr(current_bs, 1.0)
        
        new_bs_mesh = cmds.duplicate(target_mesh_final)
        cmds.parent(new_bs_mesh, new_bs_group)
        
        new_bs_mesh = cmds.rename(new_bs_mesh, name)
        cmds.move(0, 0, 0)
        cmds.DeleteHistory(new_bs_mesh)
        cmds.hide(new_bs_mesh)
        cmds.setAttr(current_bs, 0)
        
    cmds.delete(target_mesh_final)
    cmds.DeleteHistory()
        
    return new_bs_group
        

def newBlendShapeNames(blendshapes):
    '''Get the name of the blendshape without the parent node name.'''
    name = blendshapes.split('.')
    
    # returns attribute blendshape string without parent name
    return name[1]