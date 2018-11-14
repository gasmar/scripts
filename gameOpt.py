'''
* AUTHOR: Gretchen Asmar *

MESH OPTIMIZER FOR GAME ENGINES

Optimizes and cleans up meshes for game engine use.

INSTRUCTIONS:
- select mesh(es) with locally desired pivot position
- run script, it will:
    prompt to soften edges
    snap to center of grid
    freeze transformations
    delete history
'''

from maya import cmds

# elected objects
objs = cmds.ls(os=True)


def gameOpt():

    # dialogue box
    softenEdgeDialogue = cmds.confirmDialog(
        t='Soften Edges',
        b=['Yes', 'No'],
        defaultButton='Yes',
        cancelButton='No',
        dismissString='No')

    # soften the mesh's edges, should the user click 'Yes'
    if softenEdgeDialogue == 'Yes':
        for i in objs:
            cmds.select(i)
            cmds.polySoftEdge(a=180)

    # run optimization commands for game engine
    for i in objs:
        cmds.select(i)
        cmds.snapMode(gr=True)
        cmds.move(rpr=True)
        cmds.snapMode(gr=False)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.DeleteHistory()
    # deselect
    cmds.select(clear=True)


gameOpt()