'''
* AUTHOR: Gretchen Asmar *

CONSTRAIN MANY TO PARENT

Creates constraints from one parent to many children
without having to re-select children. Supports maintain
offset.

INSTRUCTIONS:
First, select objects to constrain, then target parent.
'''

from maya import cmds

selObj = cmds.ls(sl=True)


def cnsObj(mode, offset):

    # target parent
    dest = selObj[-1]
    for i in range(len(selObj)):

        currentObj = selObj[i]
        breakLen = len(selObj) - 1

        # break loop if iterated through whole selection
        if i == breakLen:
            break

        # constraint types
        if mode == "Point":
            cmds.pointConstraint(dest, currentObj, maintainOffset=offset)
            print "%s ptCns --> %s" % (currentObj, dest)
        elif mode == "Orient":
            cmds.orientConstraint(dest, currentObj, maintainOffset=offset)
            print "%s ornCns --> %s" % (currentObj, dest)
        elif mode == "Scale":
            cmds.scaleConstraint(dest, currentObj, maintainOffset=offset)
            print "%s sclCns --> %s." % (currentObj, dest)
        elif mode == "Parent":
            cmds.parentConstraint(dest, currentObj, maintainOffset=offset)
            print "%s prnCns --> %s." % (currentObj, dest)
        elif mode == "Parent and Scale":
            cmds.parentConstraint(dest, currentObj, maintainOffset=offset)
            cmds.scaleConstraint(dest, currentObj, maintainOffset=offset)
            print "%s prnCns and sclCns --> %s." % (currentObj, dest)

        # invalid user input (just to play it safe :P)
        else:
            cmds.error("Invalid.")


def showToolWindow():

    name = "ConstraintType"
    window = cmds.window(name, w=60, h=60, s=True, query=True, exists=True)
    # check for existing window, close and reopen
    if window:
        cmds.deleteUI(name)

    # UI
    cmds.window(name)

    column = cmds.columnLayout()
    cmds.frameLayout(label="Choose constraint type.")

    # Choose constraint type(s)
    cmds.columnLayout(adjustableColumn=True)
    cmds.radioCollection("constraintTypes")
    cmds.radioButton(label="Point", select=True)
    cmds.radioButton(label="Orient")
    cmds.radioButton(label="Scale")
    cmds.radioButton(label="Parent")
    cmds.radioButton(label="Parent and Scale")
    # Maintain offset checkbox
    cmds.checkBox("cnsOffsetCB", label="Maintain Offset", value=True)
    # Constrain or Close
    cmds.button(label="Constrain", command=onConstrainClick)
    cmds.button(label="Close", command=onCloseClick)

    cmds.setParent(column)
    cmds.showWindow()


def onConstrainClick(*args):

    # query values from UI
    radio = cmds.radioCollection("constraintTypes", query=True, select=True)
    mode = cmds.radioButton(radio, query=True, label=True)
    offset = cmds.checkBox("cnsOffsetCB", query=True, value=True)

    # constrain based on user input
    cnsObj(mode, offset)
    # close window and select target parent
    cmds.deleteUI("ConstraintType")
    cmds.select(selObj[-1])


def onCloseClick(*args):

    # cancel operation
    cmds.deleteUI("ConstraintType")


def notEnoughObjs(*args):

    # prompt the user to select 2 objects or more
    cmds.confirmDialog(
        title="Not enough objects",
        message="Please select at least one target and destination.",
        button="OK",
        dismissString="OK")


if len(selObj) < 2:
    notEnoughObjs()
else:
    showToolWindow()