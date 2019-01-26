'''
* AUTHOR: Gretchen Asmar *

Select all controllers (or objects) you want to zero out and run code.
'''

from maya import cmds

# selected object transforms
selObj = cmds.ls(sl=True, typ='transform')
objs = len(selObj)

for i in range(objs):
    # accessible attributes
    # these flags will keep unwanted attributes untouched
    objAttrs = cmds.listAttr(selObj[i], w=True, s=True, v=True, c=True, k=True, u=True, se=True, o=True, lf=True)
    attrs = len(objAttrs)

    for j in range(attrs):
        # find attr channel full name
        attrChannel = selObj[i] + "." + objAttrs[j]
        
        # set scale channels to 1
        if objAttrs[j] == "scaleX":
            cmds.setAttr(attrChannel, 1)
        elif objAttrs[j] == "scaleY":
            cmds.setAttr(attrChannel, 1)
        elif objAttrs[j] == "scaleZ":
            cmds.setAttr(attrChannel, 1)

        #ignore visibility
        elif objAttrs[j] == "visibility":
            continue

        #otherwise, zero out channels
        else:
            cmds.setAttr(attrChannel, 0)
