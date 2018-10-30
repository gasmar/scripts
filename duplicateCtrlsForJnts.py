'''
* AUTHOR: Gretchen Asmar *
'''

from maya import cmds

selObj = cmds.ls(sl=True)
def createCtrlsForJnts(cns, offset):

    ctrl = selObj[-1]
    newCtrls = [ctrl]

    # Duplicate control and snap to every selected joint in order
    # MUST SELECT JNT HIERARCHY IN ORDER AND CTRL LAST
    for i in range(len(selObj)):

        # First joint in hierarchy constrains the controller
        if i == 0:
            cmds.delete( cmds.parentConstraint(selObj[0], ctrl, maintainOffset=offset) )

        # check if user wants to constrain jnts
        # constrain the first selected jnt to the initial ctrl (or not) and then break loop
        elif i == len(selObj) -1 and cns == "Point":
            cmds.pointConstraint(ctrl, selObj[0], maintainOffset=True)
            break
        elif i == len(selObj) -1 and cns == "Orient":
            cmds.orientConstraint(ctrl, selObj[0], maintainOffset=True)
            break
        elif i == len(selObj) -1 and cns == "Scale":
            cmds.scaleConstraint(ctrl, selObj[0], maintainOffset=True)
            break
        elif i == len(selObj) -1 and cns == "Parent":
            cmds.parentConstraint(ctrl, selObj[0], maintainOffset=True)
            break
        elif i == len(selObj) -1 and cns == "Parent and Scale":
            cmds.parentConstraint(ctrl, selObj[0], maintainOffset=True)
            cmds.scaleConstraint(ctrl, selObj[0], maintainOffset=True)
            break
        elif i == len(selObj) -1 and cns == "Don't Constrain":
            break

        # steps to follow
        else:
            # create a new ctrl
            newCtrl = cmds.duplicate(ctrl)
            # add to list
            newCtrls.append(newCtrl)
            # snap to joint
            cmds.delete( cmds.pointConstraint( selObj[i], newCtrls[i], maintainOffset=False ) )
            # user chooses "Maintain Offset" value
            cmds.delete( cmds.parentConstraint(selObj[i], newCtrls[i], maintainOffset=offset) )

            # user has choice to constrain joints to ctrls
            if cns == "Point":
                cmds.pointConstraint(newCtrl, selObj[i], maintainOffset=True)
            elif cns == "Orient":
                cmds.orientConstraint(newCtrl, selObj[i], maintainOffset=True)
            elif cns == "Scale":
                cmds.scaleConstraint(newCtrl, selObj[i], maintainOffset=True)
            elif cns == "Parent":
                cmds.parentConstraint(newCtrl, selObj[i], maintainOffset=True)
            elif cns == "Parent and Scale":
                cmds.parentConstraint(newCtrl, selObj[i], maintainOffset=True)
                cmds.scaleConstraint(newCtrl, selObj[i], maintainOffset=True)
            elif cns == "Don't Constrain":
                continue

    # Reverse index for parenting
    newCtrls.reverse()

    # Parent ctrls from beginning to end of hierarchy
    for i in range(len(newCtrls)):

        # break loop if it reaches end of index
        if i == len(newCtrls) -1:
            break
        cmds.parent(newCtrls[i], newCtrls[i+1])
        # print "%s PARENTED TO --> %s" %(newCtrls[i], newCtrls[i+1])

    #select the ctrls in order to test immediately
    cmds.select(ctrl, hi=True)
    # freeze transformations
    cmds.makeIdentity(apply=True)

def showToolWindow():

    # window display
    name = "Constraints"
    window = cmds.window(name, width=200, height=55, s=True, query=True, exists=True)

    # if window exists, close and reopen
    if window:
        cmds.deleteUI(name)

    # interface
    cmds.window(name)

    # choose type of constraint from ctrls to jnts (if any)
    column = cmds.columnLayout(adjustableColumn=True)
    cmds.radioCollection("constraintTypes")
    cmds.radioButton(label="Point", select=True)
    cmds.radioButton(label="Orient")
    cmds.radioButton(label="Scale")
    cmds.radioButton(label="Parent")
    cmds.radioButton(label="Parent and Scale")
    cmds.radioButton(label="Don't Constrain")
    offsetCB = cmds.checkBox("cnsOffsetCB", label="Maintain Offset", value=False)

    # Constrain or Cancel operation
    cmds.button(label="Constrain", command=onConstrainClick)
    cmds.button(label="Cancel", command=onCloseClick)

    cmds.setParent(column)
    cmds.showWindow()

# Constrain
def onConstrainClick(*args):
    radio = cmds.radioCollection("constraintTypes", query=True, select=True)
    cns = cmds.radioButton(radio, query=True, label=True)
    offset = cmds.checkBox("cnsOffsetCB", query=True, value=True)
    cmds.deleteUI("Constraints")

    createCtrlsForJnts(cns, offset)

# Cancel
def onCloseClick(*args):
    cmds.deleteUI("Constraints")

if len(selObj) <1:
    cmds.confirmDialog(t="No shapes selected", m="Select objects." )
elif len(selObj) < 2:
    cmds.confirmDialog(t="Not enough objects", m="Select object(s) or joint(s) and lastly, controller.")
else:
    showToolWindow()