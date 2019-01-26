'''
* AUTHOR: Gretchen Asmar *
'''

from maya import cmds

selObj = cmds.ls(sl=True)

def cnsObj(mode, offset):
    
    dest = selObj[-1]
    for i in range(len(selObj)):
        
        currentObj = selObj[i]
        breakLen = len(selObj) - 1

        if i == breakLen:
            break
        if mode == "Point":
            cmds.pointConstraint(dest, currentObj, maintainOffset=offset)
            print "%s ptCns --> %s" %(currentObj, dest)
        elif mode == "Orient":
            cmds.orientConstraint(dest, currentObj, maintainOffset=offset)
            print "%s ornCns --> %s" %(currentObj, dest)
        elif mode == "Scale":
            cmds.scaleConstraint(dest, currentObj, maintainOffset=offset)
            print "%s sclCns --> %s." %(currentObj, dest)
        elif mode == "Parent":
            cmds.parentConstraint(dest, currentObj, maintainOffset=offset)
            print "%s prnCns --> %s." %(currentObj, dest)
        elif mode == "Parent and Scale":
            cmds.parentConstraint(dest, currentObj, maintainOffset=offset)
            cmds.scaleConstraint(dest, currentObj, maintainOffset=offset)
            print "%s prnCns and sclCns --> %s." %(currentObj, dest)
        else:
            cmds.error("Invalid.")
    
def showToolWindow():
    
    name = "ConstraintType"
    window = cmds.window(name, w=60, h=60, s=True, query=True, exists=True)
    if window:
        cmds.deleteUI(name)
    
    cmds.window(name)
    
    column = cmds.columnLayout()
    cmds.frameLayout(label="Choose constraint type.")
    
    cmds.columnLayout(adjustableColumn=True)
    cmds.radioCollection("constraintTypes")
    cmds.radioButton(label="Point", select=True)
    cmds.radioButton(label="Orient")
    cmds.radioButton(label="Scale")
    cmds.radioButton(label="Parent")
    cmds.radioButton(label="Parent and Scale")

    cmds.checkBox("cnsOffsetCB", label="Maintain Offset", value=True)

    cmds.button(label="Constrain", command=onConstrainClick)
    cmds.button(label="Close", command=onCloseClick)

    cmds.setParent(column)
    cmds.showWindow()
    

def onConstrainClick(*args):
    print "ONCONSTRAINCLICK"
    radio = cmds.radioCollection("constraintTypes", query=True, select=True)
    mode = cmds.radioButton(radio, query=True, label=True)
    offset = cmds.checkBox("cnsOffsetCB", query=True, value=True)

    cnsObj(mode, offset)
    cmds.deleteUI("ConstraintType")
    cmds.select(selObj[-1])
    print "Selected DEST"

def onCloseClick(*args):
    cmds.deleteUI("ConstraintType")

def notEnoughObjs(*args):
    cmds.confirmDialog(
        title="Not enough objects",
        message = "Please select at least one target and destination.",
        button="OK",
        dismissString="OK"
    )

if len(selObj) < 2:
    notEnoughObjs()
else:
    showToolWindow()
