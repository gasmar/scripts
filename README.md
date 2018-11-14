# Python tools and scripts for Maya

This repo is meant to aid me in studing and researching new methods for Python scripting in Maya.

## Installation

### Requirements
* Maya (2014+ recommended)

## Tools and Scripts

### zeroAttrs
Select control(s) and run to zero out every unlocked transform and attribute, including customs such as enums.

### combineShapes (WIP)
Select shapes (mostly meant for nurbs) to combine into a single node.

### constraintTypeToMany
Select target(s) and lastly destination. Run script to show dialog window. Choose params and constrain.

User can choose constraint type and whether or not to maintain offset.

### duplicateCtrlsForJnts (WIP)
Select object(s) and lastly, a controller to constrain them to. This script is very effective for quickly creating controllers and constraining joints to them.

User can choose constraint type (or deny constraint, effective for positionint and alignment) and whether to maintain offset via tool GUI.

### gameOpt.py
Simple tool to optimize meshes for game engines.

Script prompts user to smooth meshes, then moves to center of world (based on object pivot), freezes transforms and deletes history.

### renderShapes
Turns render stats on or off for selected object(s).

## Contributing
Pull requests are welcome but most of all I would appreciate fundamental and structural advice for the code. I'm still learning the proper way to design and structure code so any tips would rock my world! :D