from PySide2 import QtCore as qc
from PySide2 import QtGui as qg
from PySide2 import QtWidgets as qw
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from maya import cmds

        
class Dialog(qw.QDialog):
    '''Main dialog class.'''
    WINDOW_TITLE = 'Dialog Template'
    
    MINIMUM_WIDTH = 200
    MINIMUM_HEIGHT = 200
    
    dialog_instance = None
    
    @classmethod
    def showDialog(cls):
        '''Evaluates if dialog exists and either shows or raises it.'''
        if not cls.dialog_instance:
            cls.dialog_instance = Dialog()
        
        if cls.dialog_instance.isHidden():
            cls.dialog_instance.show()
        else:
            cls.dialog_instance.raise_()
            cls.dialog_instance.activateWindow()
    
    def mayaMainWindow():
        '''Get Maya main window in memory to parent the ui to.'''
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), qw.QWidget)
        
    def __init__(self, parent=mayaMainWindow()):
        '''Init method. Set basic credentials here.'''
        super(Dialog, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        
        # Check OS to assign proper windowFlags
        if cmds.about(ntOS=True) or cmds.about(linux=True):
            self.setWindowFlags(self.windowFlags() ^ qc.Qt.WindowContextHelpButtonHint)        
        elif cmds.about(macOS=True):
            self.setWindowFlags(qc.Qt.Tool)
        
        # Window position instance.
        self.geometry = None

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        '''Add widgets for functionality.'''
        pass

    def createLayouts(self):
        '''Create the layouts to add the widgets to.'''
        pass

    def createConnections(self):
        '''Connect the widgets to built-in or custom methods.'''
        pass
        
    def showEvent(self, event):
        '''Event to signal showing of window (for position purposes).'''
        super(Dialog, self).showEvent(event)
        
        if self.geometry:
            self.restoreGeometry(self.geometry)
    
    def closeEvent(self, event):
        '''Event to signal closing of window (for position purposes).'''
        if isinstance(self, Dialog):
            super(Dialog, self).closeEvent(event)
            
            self.geometry = self.saveGeometry()


if __name__ == '__main__':
    '''Used if called from the script editor. 
       checks memory for existing dialog and
       deletes it from memory.'''
    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass
        
    dialog = Dialog()
    dialog.show()