'''
pathAnimation -fractionMode true -follow true -followAxis x -upAxis y -worldUpType "vector" -worldUpVector 0 1 0 -inverseUp false -inverseFront false -bank false -startTimeU `playbackOptions -query -minTime` -endTimeU  `playbackOptions -query -maxTime`;

select -addFirst motionPath1;

CBdeleteConnection "motionPath1.u";

setAttr "motionPath1.uValue" .5;

CBdeleteConnection "locator1.rx";
CBdeleteConnection "locator1.ry";
CBdeleteConnection "locator1.rz";

setAttr "locator1.rotateZ" 0;
setAttr "locator1.rotateX" 0;
setAttr "locator1.rotateY" 0;
'''