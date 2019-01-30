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
    
    MINIMUM_WIDTH = 380
    MINIMUM_HEIGHT = 106
    BTN_HEIGHT = 26
    
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
        
            
    def __init__(self, parent = mayaMainWindow()):
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
        
        self.clear_btn      = qw.QPushButton('Clear')
        self.clear_btn.setToolTip('Clear selection line.')
        self.clear_btn.setFixedHeight(self.BTN_HEIGHT)
        
        self.option_combobox = qw.QComboBox()
        self.option_combobox.addItems(['World axis', 'Manual'])
                
        self.create_btn     = qw.QPushButton()
        self.create_btn.setIcon(qg.QIcon(':create.png'))
        self.create_btn.setToolTip('Create')
        self.create_btn.setFixedSize(40, 26)
        
        self.connect_btn    = qw.QPushButton()
        self.connect_btn.setIcon(qg.QIcon(':mergeConnections.png'))
        self.connect_btn.setToolTip('Connect')
        self.connect_btn.setFixedSize(40, 26)
        
        self.disconnect_btn = qw.QPushButton()
        self.disconnect_btn.setIcon(qg.QIcon(':deletePoint.png'))
        self.disconnect_btn.setToolTip('Break auto rotation connections and delete nodes.')
        self.disconnect_btn.setFixedSize(40, 26)
        
        self.z_radio        = qw.QRadioButton('Z')
        self.z_radio.setChecked(True)
        self.z_neg_radio    = qw.QRadioButton('-Z')
        self.x_radio        = qw.QRadioButton('X')
        self.x_neg_radio    = qw.QRadioButton('-X')
        
        self.rotate_slider  = qw.QSlider()
        self.rotate_slider.setFixedWidth(180)
        self.rotate_slider.setRange(-360, 360)
        self.rotate_slider.setOrientation(qc.Qt.Horizontal)
        self.rotate_slider.setVisible(False)
        
        self.rotate_spin    = qw.QSpinBox()
        self.rotate_spin.setRange(-360, 360)
        self.rotate_spin.setFixedWidth(50)
        self.rotate_spin.setVisible(False)
        
        self.cancel_btn     = qw.QPushButton('Cancel')
        self.cancel_btn.setFixedHeight(self.BTN_HEIGHT)
        

    def createLayouts(self):
        '''Layouts to hold widgets.'''
        main_layout      = qw.QVBoxLayout(self)

        selection_layout = qw.QHBoxLayout(self)
        selection_layout.addWidget(self.name_label)
        selection_layout.addWidget(self.line_edit)
        selection_layout.addWidget(self.add_btn)
        selection_layout.addWidget(self.clear_btn)
        
        buttons_layout   = qw.QHBoxLayout(self)
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.connect_btn)
        buttons_layout.addWidget(self.disconnect_btn)
        buttons_layout.addSpacerItem(qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding))
        buttons_layout.addWidget(self.cancel_btn)
        
        rotate_layout    = qw.QHBoxLayout(self)
        rotate_layout.addWidget(self.option_combobox)
        rotate_layout.addSpacerItem(qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding))
        rotate_layout.addWidget(self.z_radio)
        rotate_layout.addWidget(self.z_neg_radio)
        rotate_layout.addWidget(self.x_radio)
        rotate_layout.addWidget(self.x_neg_radio)
        rotate_layout.addWidget(self.rotate_slider)
        rotate_layout.addWidget(self.rotate_spin)
        rotate_layout.setSpacing(20)
        rotate_layout.setContentsMargins(0, 10, 0, 10)
        rotate_layout.addStretch()
        
        main_layout.addLayout(selection_layout)
        main_layout.addLayout(rotate_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(5)
        main_layout.setAlignment(qc.Qt.AlignTop)
        

    def createConnections(self):
        '''Emitted signals for functionality.'''
        self.add_btn.clicked.connect(self.onAddSelection)
        self.clear_btn.clicked.connect(self.onClear)
        
        self.option_combobox.currentIndexChanged.connect(self.onOption)
        
        self.rotate_slider.valueChanged.connect(self.rotate_spin.setValue)
        self.rotate_spin.valueChanged.connect(self.rotate_slider.setValue)
                
        self.create_btn.clicked.connect(self.onCreateClick)
        self.connect_btn.clicked.connect(self.onConnectClick)
        self.disconnect_btn.clicked.connect(self.onDisconnectClick)
        self.cancel_btn.clicked.connect(self.close)


    def onAddSelection(self):
        '''Add selection string to line_edit.'''
        selection = aru.selection()
        
        if selection == False:
            return cmds.warning('Please select object(s) to add to list.')
            
        self.line_edit.setText(selection)
        
    def onClear(self):
        '''Clear line_edit text.'''
        self.line_edit.setText('')
        
    def onOption(self, index):
        '''Toggle visibility for wheel orientation options.'''
        self.rotate_spin.setVisible(index)
        self.rotate_slider.setVisible(index)
        
        self.z_radio.setVisible(not(index))
        self.z_neg_radio.setVisible(not(index))
        self.x_radio.setVisible(not(index))
        self.x_neg_radio.setVisible(not(index))


    def onCreateClick(self):
        '''Create nodes for wheel rotation.'''
        targets = self.line_edit.text()
        targets = targets.split(' ')
        
        for trg in targets:
            # check for false target or no target at all
            if not trg:
                return cmds.warning('No target assigned.')
            elif cmds.objExists(trg) == False:
                cmds.warning(trg, ' doesn\'t exist.')
                continue
                
            # check for auto rotate setup on current target
            check_base = autoRotate.checkForAutoRotateBase(trg)
            check_connections = autoRotate.checkForAutoRotateConnections(trg)
            
            # target is connected to an auto rotation system
            if check_base == True or check_connections == True:
                cmds.warning('Object is already connected to an auto rotation system.')
                continue
                
            check_parent = aru.checkParent(trg)
            # if no parent, target is grouped to a world level node
            if check_parent != True:
                name=check_parent
                cmds.group(trg, name=name)
                
            autoRotate.base(trg)
            cmds.select(clear=True)
            
    def onConnectClick(self):
        
        targets = self.line_edit.text()
        targets = targets.split(' ')
        
        for trg in targets:
            # check for false target or no target at all
            if not trg:
                return cmds.warning('No target assigned.')
            elif cmds.objExists(trg) == False:
                return cmds.warning(trg, ' doesn\'t exist.')
            else:
                "EVERYTHING'S COOL :DDDDDDDDDDDD"
                
            # check for auto rotate setup on current target
            check_connection = autoRotate.checkForAutoRotateConnections(trg)
            
            # target is connected to an auto rotation system
            if check_connection == True:
                return cmds.warning('Object is already connected to an auto rotation system.')
                
            # autoRotate.base(trg)
            autoRotate.autoRotate(trg)
            cmds.select(clear=True)
            
    def onDisconnectClick(self):
        '''Delete all nodes related to autoRotate and parent initial geo to the world.'''
        targets = self.line_edit.text()
        targets = targets.split(' ')
        
        for trg in targets:
            # check for false target or no target at all
            if not trg:
                return cmds.warning('No target assigned.')
            elif cmds.objExists(trg) == False:
                return cmds.warning(trg, ' doesn\'t exist.')
            # check for auto rotate setup on current target
            check_connection = autoRotate.checkForAutoRotateBase(trg)
            
            autoRotate.deleteAutoRotate(trg)
            
        
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