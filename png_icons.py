from maya import cmds

for item in cmds.resourceManager(nameFilter='*png'):
    print item