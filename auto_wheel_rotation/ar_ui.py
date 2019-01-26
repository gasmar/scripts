from PySide2 import QtCore as qc
from PySide2 import QtGui as qg
from PySide2 import QtWidgets as qw
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from maya import cmds

from auto_wheel_rotation import autoRotate
reload(autoRotate)
from auto_wheel_rotation.utils import ar_utils as aru
reload(aru)

        
class AutoRotateDialog(qw.QDialog):
    '''Main dialog class.'''
    WINDOW_TITLE = 'Auto Rotate'
    
    MINIMUM_WIDTH = 250
    MINIMUM_HEIGHT = 120
    
    dialog_instance = None
    
    @classmethod
    def showDialog(cls):
        '''Evaluates if dialog exists and either shows or raises it.'''
        if not cls.dialog_instance:
            cls.dialog_instance = AutoRotateDialog()
        
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
        super(AutoRotateDialog, self).__init__(parent)
        
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
        '''Widgets for functionality.'''
        self.name_label     = qw.QLabel('wheel:')
        
        self.line_edit      = qw.QLineEdit()
        self.line_edit.setPlaceholderText('Enter wheel objects...')
        
        self.add_btn        = qw.QPushButton()
        self.add_btn.setIcon(qg.QIcon(':selectObject.png'))
        self.add_btn.setToolTip('Add selection.')
        
        self.create_btn     = qw.QPushButton()
        self.create_btn.setIcon(qg.QIcon(':create.png'))
        self.create_btn.setToolTip('Create')
        
        self.connect_btn     = qw.QPushButton()
        self.connect_btn.setIcon(qg.QIcon(':mergeConnections.png'))
        self.connect_btn.setToolTip('Connect')
        
        self.disconnect_btn  = qw.QPushButton()
        self.disconnect_btn.setIcon(qg.QIcon(':deletePoint.png'))
        self.disconnect_btn.setToolTip('Break auto rotation connections and delete nodes.')
        
        self.create_btn.setToolTip('Create')
        self.cancel_btn     = qw.QPushButton('Cancel')
        
        self.z_radio        = qw.QRadioButton('Z')
        self.z_radio.setChecked(True)
        self.z_neg_radio    = qw.QRadioButton('-Z')
        self.x_radio        = qw.QRadioButton('X')
        self.x_neg_radio    = qw.QRadioButton('-X')

    def createLayouts(self):
        '''Layouts to hold widgets.'''
        main_layout      = qw.QVBoxLayout(self)

        selection_layout = qw.QHBoxLayout(self)
        selection_layout.addWidget(self.name_label)
        selection_layout.addWidget(self.line_edit)
        selection_layout.addWidget(self.add_btn)

        buttons_layout   = qw.QHBoxLayout(self)
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.connect_btn)
        buttons_layout.addWidget(self.disconnect_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addStretch()
        
        radio_layout     = qw.QHBoxLayout(self)
        radio_layout.addWidget(self.z_radio)
        radio_layout.addWidget(self.z_neg_radio)
        radio_layout.addWidget(self.x_radio)
        radio_layout.addWidget(self.x_neg_radio)
        radio_layout.setSpacing(40)
        radio_layout.setContentsMargins(0, 10, 0, 10)
        radio_layout.addStretch()

        main_layout.addLayout(selection_layout)
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setContentsMargins(5, 10, 5, 10)
        main_layout.setSpacing(10)
        main_layout.setAlignment(qc.Qt.AlignTop)

    def createConnections(self):
        '''Emitted signals for functionality.'''
        self.add_btn.clicked.connect(self.onAddSelection)
        self.create_btn.clicked.connect(self.onCreateClick)
        self.connect_btn.clicked.connect(self.onConnectClick)
        self.disconnect_btn.clicked.connect(self.onDisconnectClick)
        self.cancel_btn.clicked.connect(self.close)


    def onAddSelection(self):
        '''Add selection string to line_edit.'''
        selection = aru.selection()
        self.line_edit.setText(selection)

    def onCreateClick(self):
        '''Create nodes for wheel rotation.'''
        targets = self.line_edit.text()
        targets = targets.split(' ')
        
        for each in targets:
            # check for a parent
            check_parent = aru.checkParent(each)
            # check if target(s) have an auto rotate setup
            check_connection = aru.checkForExistingAutoRotate(each)
            
            if check_connection == True:
                cmds.warning('Object is already connected to an auto rotation system.')    
                continue
                
            if check_parent != True:
                # if no parent, target is grouped to a world level node
                name=check_parent
                cmds.group(each, name=name)
                
            autoRotate.base(each)
            autoRotate.autoRotate(each)
            
    def onConnectClick(self):
        # TODO:
        # Separate base() and autoRotate() functions
        pass
            
    def onDisconnectClick(self):
        '''Delete all nodes related to autoRotate and parent initial geo to the world.'''
        targets = self.line_edit.text()
        targets = targets.split(' ')
        
        for each in targets:            
            autoRotate.deleteAutoRotate(each)
        
    def showEvent(self, event):
        '''Event to signal showing of window (for position purposes).'''
        super(AutoRotateDialog, self).showEvent(event)
        
        if self.geometry:
            self.restoreGeometry(self.geometry)
    
    def closeEvent(self, event):
        '''Event to signal closing of window (for position purposes).'''
        if isinstance(self, AutoRotateDialog):
            super(AutoRotateDialog, self).closeEvent(event)
            
            self.geometry = self.saveGeometry()


if __name__ == '__main__':
    '''Used if called from the script editor. 
       checks memory for existing dialog and
       deletes it from memory.'''
    try:
        arui.close()
        arui.deleteLater()
    except:
        pass
        
    arui = AutoRotateDialog()
    arui.show()