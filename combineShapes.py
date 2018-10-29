'''
* AUTHOR: Gretchen Asmar *

Creates a single object fro various shapes.
Works very well with cirves for rigging ctrls.
Just select desired objects to combine and run!
'''

from maya import cmds

# objects
selObj = cmds.ls(sl=True)
# shapes
selShpObj = cmds.ls(sl=True, dag=True, s=True)


# ask user for desired shape name
def toolWindow(*args):
    promptUser = cmds.promptDialog(
        title='Rename Object',
        message='Shape Name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    name = cmds.promptDialog(query=True, text=True)

    # if name:
    #create empty group with user input name
    shpGrp = cmds.group(n=name, em=True)

    # clean up separate shapes
    def createShape(group):
        for i in range(len(selShpObj)):
            cmds.delete(ch=True)
            cmds.makeIdentity(a=True)
            cmds.select()

        # select objects and empty group node
        cmds.select(selObj)
        cmds.select(group, tgl=True)
        # snap group pivot to selected shapes center and clean up
        cmds.delete(cmds.pointConstraint(maintainOffset=False))
        
        translateX = cmds.getAttr(shpGrp + ".translateX")
        translateY = cmds.getAttr(shpGrp + ".translateY")
        translateZ = cmds.getAttr(shpGrp + ".translateZ")
        print "translateX", translateX
        print "translateY", translateY
        print "translateZ", translateZ
        print "shpGrp: ", group

        print "selObj: ", selObj

        cmds.makeIdentity(a=True)
        # create a single shape from initial selection
        cmds.parent(selShpObj, group, r=True, s=True)
        # delete empty nodes
        cmds.delete(selObj)

        def moveBackToOrigin(*args):    
            cmds.xform(group, centerPivots=True)
            cmds.move(translateX, translateY, translateZ)
            print "group: ", group
            cmds.makeIdentity(group, a=True)
        
        
    createShape(shpGrp)

if len(selObj) < 1:
    cmds.confirmDialog(t="No shapes selected", m="Select shapes to combine." )
elif len(selObj) < 2:
    cmds.confirmDialog(t="Not enough objects", m="Select two or more shapes to combine.")
else:
    toolWindow()