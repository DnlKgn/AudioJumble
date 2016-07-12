from PySide import QtGui, QtCore

class QJumpSlider(QtGui.QSlider):
    
    def __init__(self, *args, **kwargs):
        QtGui.QSlider.__init__(self, *args, **kwargs)
        self.mouse_pressed = False
    
    #def mouseMoveEvent(self, event):
    #    event.ignore()
        
    def mousePressEvent(self, event):
        style=self.style()
        opt=QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)
        rectHandle=style.subControlRect(QtGui.QStyle.CC_Slider,opt, QtGui.QStyle.SC_SliderHandle,self)
       
        if event.button() == QtCore.Qt.LeftButton and not rectHandle.contains(event.pos()):
            
            if self.orientation() == QtCore.Qt.Vertical:
                newVal = self.minimum() + ((self.maximum() - self.minimum()) * (self.height() - event.y())) / self.height()
            else:
                newVal = self.minimum() + ((self.maximum() - self.minimum()) * event.x()) / self.width()
            
            if self.invertedAppearance():
                print("invert")
                self.setValue(self.maximum() - newVal)
            else:
                self.setValue(newVal)
            event.accept()
            
        else:    
            super(QJumpSlider, self).mousePressEvent(event)
        #if event.button() == QtCore.Qt.LeftButton and 
    
    #def mouseGrabber(self, event):
    #    event.ignore()
    
    #def mouseDoubleClickEvent(self, event):
    #    event.ignore()
    
    #def focusInEvent(self, event):
    #    event.ignore()
        
    #def focusOutEvent(self, event):
    #    event.ignore()