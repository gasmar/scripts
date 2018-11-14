'''
* AUTHOR: Gretchen Asmar *

RENDER STATS SWITCH

Turns render stats on or off for selected object(s)
This is ideal for geometry controls!

INSTRUCTIONS:
Select object(s) and, when prompted, choose whether to 
turn render stats on or off.
'''

from maya import cmds

# selection
selObj = cmds.ls(sl=True)
objLen = len(selObj)

if selObj < 1:
    cmds.cmds.confirmDialog(t="No shapes selected", m="Select object(s).")

# confirm whether to render or not
renderDialog = cmds.confirmDialog(
    title="Render objects",
    message='Render stats for selected object(s)?',
    button=['ON', 'OFF', 'Cancel'],
    defaultButton='OFF',
    cancelButton='Cancel',
    dismissString='Cancel')

for i in range(objLen):
    # turn render stats OFF
    if renderDialog == 'OFF':
        strObj = str(selObj[i])
        cmds.setAttr(strObj + ".castsShadows", 0)
        cmds.setAttr(strObj + ".receiveShadows", 0)
        cmds.setAttr(strObj + ".motionBlur", 0)
        cmds.setAttr(strObj + ".primaryVisibility", 0)
        cmds.setAttr(strObj + ".smoothShading", 0)
        cmds.setAttr(strObj + ".visibleInReflections", 0)
        cmds.setAttr(strObj + ".visibleInRefractions", 0)
        cmds.setAttr(strObj + ".doubleSided", 0)

    # turn render stats ON
    elif renderDialog == 'ON':
        cmds.setAttr(strObj + ".castsShadows", 1)
        cmds.setAttr(strObj + ".receiveShadows", 1)
        cmds.setAttr(strObj + ".motionBlur", 1)
        cmds.setAttr(strObj + ".primaryVisibility", 1)
        cmds.setAttr(strObj + ".smoothShading", 1)
        cmds.setAttr(strObj + ".visibleInReflections", 1)
        cmds.setAttr(strObj + ".visibleInRefractions", 1)
        cmds.setAttr(strObj + ".doubleSided", 1)