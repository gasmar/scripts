"""

*Blend Shape Mirrorer* [mBS]

Instructions: 

1. Duplicate base geometry

2. Select duplicate, then shape to mirror...

3. Run code :)

"""

#import Maya Command Module
import maya.cmds as mc

#Get initial selection [destination and Blend Shape target to mirror]...
sel_initGeo = mc.ls(sl=True)

#Verify that 2 objects are selected!
if sel_initGeo < 2:
    
    #Warning message if condition isn't met
    mc.warning("Must select destination mesh, then source mesh to mirror!  ...or else x(")

#If condition is met, do the following...
else:
    
    #Select destination mesh only
    mc.select(sel_initGeo[0], r=True)
    
    #Duplicate destination mesh only [rr = return root only]
    mc.duplicate(rr=True)
    
    #Get selection of mesh to flip
    selGeo_flipSclX = mc.ls(sl=True)
    
    #Unlock Scale X of mesh so it can be flipped
    mc.setAttr((selGeo_flipSclX[0] + '.sx'), lock=False)
    
    #Flip mesh [scale mesh in -X]
    mc.setAttr((selGeo_flipSclX[0] + '.sx'), -1)
    
    #Add target geo as a Blend Shape to flipped geo
    mc.select(sel_initGeo[1], r=True)
    mc.select(selGeo_flipSclX[0], add=True)
    mc.blendShape(frontOfChain=True, n="targetToFlip")
    
    #Wrap deform destination mesh to flipped mesh
    mc.select(sel_initGeo[0], r=True)
    mc.select(selGeo_flipSclX[0], add=True)
    #Note: In Python, "()" should immediately follow a command in order for the command to work properly; even if nothing is defined inside of "()"
    mc.CreateWrap()
    
    #Activate Blend Shape
    mc.setAttr(("targetToFlip" + "." + sel_initGeo[1]), 1)
    
    #Clean up
    mc.delete(sel_initGeo[0], ch=True)
    #NOTE: we must delete flipped mesh AND its hidden base node generated from Wrap Deformer
    mc.delete((selGeo_flipSclX[0]), (selGeo_flipSclX[0] + "Base"))
    
    
    #Reminder:
    mc.headsUpMessage("End!  Remember to rename your mirrored shape and store it in your Blend Shapes group :)")
    print ("End!  Remember to rename your mirrored shape and store it in your Blend Shapes group :)")
    