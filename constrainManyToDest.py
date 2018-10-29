'''
* AUTHOR: Gretchen Asmar *
'''

from maya import cmds

def cnsScale():
    selObj = cmds.ls(sl=True)
    dest = selObj[-1]
    breakLen = len(selObj) - 1
    
    for i in range(len(selObj)):
        
        currentObj = selObj[i]
        
        if i == breakLen:
            break
            
        cmds.scaleConstraint(dest, currentObj)
        print "%s sclCnst --> %s." %(currentObj, dest)

cnsScale()