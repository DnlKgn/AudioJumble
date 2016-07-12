import sys
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import settings
import threading
import audio_jumbler
import QJumpSlider

class AudioJumbleUIMain(QtGui.QWidget):
    
    dataChanged = QtCore.Signal()
    
    def __init__(self, aj):
        super(AudioJumbleUIMain, self).__init__()
        self.aj = aj
        self.initUI()
    
    def initUI(self):
        self.resize(900, 400)
        self.setWindowTitle('Audio Jumble GUI')
    
        self.center()
    
        playButton = QtGui.QPushButton("Play")
        pauseButton = QtGui.QPushButton("Pause")
        continueButton = QtGui.QPushButton("Continue")
        addButton = QtGui.QPushButton("Add")
        removeButton = QtGui.QPushButton("Remove")

        self.musicProgressBar = QJumpSlider.QJumpSlider(QtCore.Qt.Horizontal, self)
        #self.musicProgressBar = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_is_pressed = False
        #self.musicProgressBar.setTextVisible(False)
        
        self.fileList = QtGui.QListWidget()

        musicButtonsHbox = QtGui.QHBoxLayout()
        
        musicButtonsControlHbox = QtGui.QHBoxLayout()
        
        musicButtonsControlHbox.addWidget(playButton)
        musicButtonsControlHbox.addWidget(pauseButton)
        musicButtonsControlHbox.addWidget(continueButton)
        musicButtonsHbox.addWidget(addButton)
        musicButtonsHbox.addWidget(removeButton)

        musicVBox = QtGui.QVBoxLayout()
        musicVBox.addWidget(self.fileList)
        musicVBox.addWidget(self.musicProgressBar)
        musicVBox.addLayout(musicButtonsHbox)
        musicVBox.addLayout(musicButtonsControlHbox)
        
        optionsGrid = QtGui.QGridLayout()
        
        lblGlitchProbName = QtGui.QLabel(self)
        lblGlitchProbName.setText("Glitch Probability: ")
        self.txtGlitchProb = QtGui.QLineEdit(self)
        self.txtGlitchProb.setFixedWidth(100)
        
        lblGlitchDurationName = QtGui.QLabel(self)
        lblGlitchDurationName.setText("Glitch Duration: ")
        self.txtGlitchDuration = QtGui.QLineEdit(self)
        self.txtGlitchDuration.setFixedWidth(100)
        
        ## PITCH
        # initial pitch
        lblStartPitch = QtGui.QLabel(self)
        lblStartPitch.setText("Initial Pitch: ")
        self.txtStartPitch = QtGui.QLineEdit(self)
        self.txtStartPitch.setFixedWidth(100)
        
        # min pitch
        lblMinPitch = QtGui.QLabel(self)
        lblMinPitch.setText("Min Pitch: ")
        self.txtMinPitch = QtGui.QLineEdit(self)
        self.txtMinPitch.setFixedWidth(100)
        
        # max pitch
        lblMaxPitch = QtGui.QLabel(self)
        lblMaxPitch.setText("Max Pitch: ")
        self.txtMaxPitch = QtGui.QLineEdit(self)
        self.txtMaxPitch.setFixedWidth(100)
        
        # pitch change chance
        lblChancePitch = QtGui.QLabel(self)
        lblChancePitch.setText("Pitch Chance: ")
        self.txtChancePitch = QtGui.QLineEdit(self)
        self.txtChancePitch.setFixedWidth(100)
        
        # pitch change speed
        lblSpeedPitch = QtGui.QLabel(self)
        lblSpeedPitch.setText("Pitch Speed: ")
        self.txtSpeedPitch = QtGui.QLineEdit(self)
        self.txtSpeedPitch.setFixedWidth(100)
        
        # min wait
        lblMinWait= QtGui.QLabel(self)
        lblMinWait.setText("Min Wait: ")
        self.txtMinWait = QtGui.QLineEdit(self)
        self.txtMinWait.setFixedWidth(100)
        
        
        lblDisplayCurrentPitchName = QtGui.QLabel("Pitch: ")
        self.lblDisplayCurrentPitch = QtGui.QLabel("N/A")
        
        self.lblStatus = QtGui.QLabel("")
        btnApplySettings = QtGui.QPushButton("Apply")
        
        #glitchButton = QtGui.QPushButton("Glitch")
        
        optionsGrid.addWidget(lblGlitchProbName, 0, 0)
        optionsGrid.addWidget(self.txtGlitchProb, 0, 1)
        optionsGrid.setAlignment(self.txtGlitchProb, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblGlitchDurationName, 1, 0)
        optionsGrid.addWidget(self.txtGlitchDuration, 1, 1)
        optionsGrid.setAlignment(self.txtGlitchDuration, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblStartPitch, 2, 0)
        optionsGrid.addWidget(self.txtStartPitch, 2, 1)
        optionsGrid.setAlignment(self.txtStartPitch, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblMaxPitch, 3, 0)
        optionsGrid.addWidget(self.txtMaxPitch, 3, 1)
        optionsGrid.setAlignment(self.txtMaxPitch, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblMinPitch, 4, 0)
        optionsGrid.addWidget(self.txtMinPitch, 4, 1)
        optionsGrid.setAlignment(self.txtMinPitch, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblChancePitch, 5, 0)
        optionsGrid.addWidget(self.txtChancePitch, 5, 1)
        optionsGrid.setAlignment(self.txtChancePitch, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblSpeedPitch, 6, 0)
        optionsGrid.addWidget(self.txtSpeedPitch, 6, 1)
        optionsGrid.setAlignment(self.txtSpeedPitch, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblMinWait, 7, 0)
        optionsGrid.addWidget(self.txtMinWait, 7, 1)
        optionsGrid.setAlignment(self.txtMinWait, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(lblDisplayCurrentPitchName, 8, 0)
        optionsGrid.addWidget(self.lblDisplayCurrentPitch, 8, 1)
        optionsGrid.setAlignment(self.lblDisplayCurrentPitch, QtCore.Qt.AlignLeft)
        
        optionsGrid.addWidget(btnApplySettings, 9, 0)
        optionsGrid.setAlignment(btnApplySettings, QtCore.Qt.AlignBottom)
        optionsGrid.addWidget(self.lblStatus, 9, 1)
        optionsGrid.setAlignment(self.lblStatus, QtCore.Qt.AlignBottom)
        
        mainHBox = QtGui.QHBoxLayout()
        
        mainHBox.addLayout(musicVBox)
        mainHBox.setAlignment(musicVBox, QtCore.Qt.AlignCenter)
        mainHBox.addLayout(optionsGrid)
        mainHBox.setAlignment(optionsGrid, QtCore.Qt.AlignRight)
        
        self.setLayout(mainHBox)    
        
        self.load_values()
        
        btnApplySettings.pressed.connect(self.apply_values)
        
        playButton.pressed.connect(self.play)
        pauseButton.pressed.connect(self.pause)
        continueButton.pressed.connect(self.continue_play)
        
        addButton.pressed.connect(self.handleListSelect)
        removeButton.pressed.connect(self.removeSongs)
        
        addButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        removeButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        playButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        pauseButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        continueButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        
        btnApplySettings.setFocusPolicy(QtCore.Qt.ClickFocus)
        
        self.musicProgressBar.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.fileList.setFocusPolicy(QtCore.Qt.ClickFocus)
        
        self.dataChanged.connect(self.dataChangedSlot)
        self.musicProgressBar.valueChanged[int].connect(self.musicPositionChanged)
        self.musicProgressBar.sliderPressed.connect(self.musicSliderPressed)
        self.musicProgressBar.sliderReleased.connect(self.musicSliderReleased)
        self.fileList.doubleClicked.connect(self.play)
        
        self.setUpTabs()
        
        self.show()
    
    def setUpTabs(self):
        
        self.setTabOrder(self.txtGlitchProb, self.txtGlitchDuration)
        self.setTabOrder(self.txtGlitchDuration, self.txtStartPitch)
        self.setTabOrder(self.txtStartPitch, self.txtMaxPitch)
        self.setTabOrder(self.txtMaxPitch, self.txtMinPitch)
        self.setTabOrder(self.txtMinPitch, self.txtChancePitch)
        self.setTabOrder(self.txtChancePitch, self.txtSpeedPitch)
        self.setTabOrder(self.txtSpeedPitch, self.txtMinWait)
        #self.setTabOrder(self.txtMinWait, self.txtGlitchProb)
        
    def musicPositionChanged(self, value):
        #if self.aj.env:
        #    self.aj.env.events.append(("music:position:change", value))
        if not self.slider_is_pressed:
            self.seek(value)
            
    def seek(self, value):
        self.aj.enter_critical()
        if self.aj.env and self.aj.playing:
            settings.DO_SEEK = True
            pos = (value / self.aj.env.track.frames)
            settings.SEEK_TO = self.aj.env.track.runtime * pos
            self.aj.leave_critical()
            self.aj.seek()
            return
        self.aj.leave_critical()
    
    def musicSliderPressed(self):
        #print("pressed")
        self.slider_is_pressed = True
        #if self.aj.playing:
        #    self.aj.stop()
        
    def musicSliderReleased(self):
        #print("released")
        self.slider_is_pressed = False
        self.seek(self.musicProgressBar.value())
        
    def glitchProbablityValueChanged(self, val):
        self.lblGlitchProb.setText('{:04.2f}'.format((val/100.0)))

    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    @QtCore.Slot(int)
    def dataChangedSlot(self):
        if self.aj.env:
            self.lblDisplayCurrentPitch.setText(str(self.aj.env.current_pitch*100)+"%")
            #self.fileList.setCurrentRow(self.aj.at)
            self.aj.enter_critical()
            for i in range(self.fileList.count()):
                item = self.fileList.item(i)
                if item:
                    item.setForeground(QtGui.QBrush(QtCore.Qt.black))
            item = self.fileList.item(self.aj.at)
            if item:
                item.setForeground(QtGui.QBrush(QtCore.Qt.blue))
            self.aj.leave_critical()
            #print(self.aj.env.current_frame, self.aj.env.total_frames, )
            if not self.slider_is_pressed:
                self.musicProgressBar.blockSignals(True)
                self.musicProgressBar.setRange(0, int(self.aj.env.track.frames))
                self.musicProgressBar.setValue(int(self.aj.env.track.frame))
                self.musicProgressBar.blockSignals(False)
        else:
            self.lblDisplayCurrentPitch.setText("N/A")
    
    def invalidate_data(self):
        self.dataChanged.emit()
        
        
    def load_values(self):
        self.txtStartPitch.setText(str(settings.PITCH_START))
            
        self.txtMinPitch.setText(str(settings.PITCH_MIN))
        self.txtMaxPitch.setText(str(settings.PITCH_MAX))
        
        self.txtChancePitch.setText(str(settings.PITCH_CHANGE_CHANCE))
        self.txtSpeedPitch.setText(str(settings.PITCH_CHANGE_SPEED))
        
        self.txtGlitchProb.setText(str(settings.GLITCH_CHANCE))
        self.txtGlitchDuration.setText(str(settings.GLITCH_DURATION))
        
        self.txtMinWait.setText(str(settings.MIN_WAIT_AFTER_EVENT))
        
    def apply_values(self):
        #try:
            settings.PITCH_START = float(str(self.txtStartPitch.text()))
            
            settings.PITCH_MIN = float(str(self.txtMinPitch.text()))
            settings.PITCH_MAX = float(str(self.txtMaxPitch.text()))
            
            settings.PITCH_CHANGE_CHANCE = float(str(self.txtChancePitch.text()))
            settings.PITCH_CHANGE_SPEED = float(str(self.txtSpeedPitch.text()))
            
            settings.GLITCH_CHANCE = float(str(self.txtGlitchProb.text()))
            settings.GLITCH_DURATION = float(str(self.txtGlitchDuration.text()))
            
            settings.MIN_WAIT_AFTER_EVENT = float(str(self.txtMinWait.text()))
            
            if self.aj.env:
                self.aj.env.current_ptich = float(str(self.txtStartPitch.text()))
                
                self.aj.env.pitch_min = float(str(self.txtMinPitch.text()))
                self.aj.env.pitch_max = float(str(self.txtMaxPitch.text()))
                
                self.aj.env.pitch_change_chance = float(str(self.txtChancePitch.text()))
                self.aj.env.pitch_max_change_speed = float(str(self.txtSpeedPitch.text()))
                
                self.aj.env.glitch_chance = float(str(self.txtGlitchProb.text()))
                self.aj.env.glitch_duration = float(str(self.txtGlitchDuration.text()))
                
                self.aj.env.wait_after_event = float(str(self.txtMinWait.text()))
                
                self.lblStatus.setText("")
        #except:
            #self.lblStatus.setText("Value ERROR")
        
    def check_values(self):
        print("checking values")
        print(str(self.txtChancePitch.text()))
        self.txtSpeedPitch
        self.txtMaxPitch
        self.txtMinPitch
        self.txtStartPitch
        self.txtGlitchProb
        self.txtGlitchDuration
        
    def get_files(self):
        return [self.fileList.item(i).text() for i in range(self.fileList.count())]
            
    
    def play(self):
        indexes = [x.row() for x in self.fileList.selectedIndexes()]
        if indexes:
            index = indexes[0]
        else:
            index = 0
            
        if self.fileList.count() > 0:
            th = threading.Thread(target=self.aj.run, args=(self.get_files, index, self))
            th.start()
        
        if self.aj.env:
            self.aj.env.pause = False
    
    def pause(self):
        if self.aj.env:
            self.aj.env.pause = True
        
    def continue_play(self):
        if self.aj.env:
            self.aj.env.pause = False
        
    def closeEvent(self, event):
        self.aj.stop()
        event.accept()
        
    def handleListSelect(self):
        title = "Select Files"
        selected_files = QtGui.QFileDialog.getOpenFileNames(self, title, "", "Audio ("+" ".join(["*." + e for e in settings.EXTENSIONS])+")")[0]
        for file in selected_files:
            self.fileList.addItem(file)
            
    def removeSongs(self):
        items = self.fileList.selectedItems()
        for item in items:
            row = self.fileList.row(item)
            #print (row, self.aj.at)
            #self.aj.enter_critical()
            
            if self.aj.playing and self.aj.at == row:
                self.aj.stop()
            
            self.aj.enter_critical()
            if self.aj.at % self.fileList.count() > row:
                self.aj.at -= 1
            self.fileList.takeItem(self.fileList.row(item))
            
            self.aj.leave_critical()
            
            #self.aj.leave_critical()
            print("removing item: " + item.text())
            
def main():
    
    
    aj = audio_jumbler.AudioJumbler()
    app = QtGui.QApplication(sys.argv)
    
    app.setWindowIcon(QtGui.QIcon("AudioJumbleIcon.png"))
    
    import ctypes
    myappid = 'AudioJumble' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    ex = AudioJumbleUIMain(aj)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()