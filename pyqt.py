import sys
import Tkinter
import tkFileDialog
from thread import start_new_thread
import threading
from PyQt4 import QtCore, QtGui, uic 
import train
import time
import test
import os
global Image_path,Train_path,a
form_class = uic.loadUiType("example.ui")[0]                 # Load the UI
class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Browse)  # Bind the event handlers
        self.pushButton_3.clicked.connect(self.Browse2)  #   to the buttons
        self.pushButton_2.clicked.connect(self.final)
#	self.pushButton_4.clicked.connect(self.caltra)        
	self.label_2.setPixmap(QtGui.QPixmap("default.jpg"))
        self.label_3.setPixmap(QtGui.QPixmap("default.jpg"))
	self.progressBar.setValue(0)
	
    def Browse(self): 
        global Train_path
	self.onStart()
	self.label_2.setPixmap(QtGui.QPixmap("default.jpg"))
        self.label_3.setPixmap(QtGui.QPixmap("default.jpg"))
	self.label_6.clear()
	self.lineEdit_3.setText("")
	root = Tkinter.Tk()
	root.withdraw()                 # button event handler
	Train_path=tkFileDialog.askdirectory()		
	#filedialog= QtGui.QFileDialog()   	
	#Train_path=str(filedialog.getExistingDirectory(self,"Select Train Directory"))
	x=Train_path.split('/')
    	l=len(x)	
	self.lineEdit.setText(x[l-1])
    	self.caltra()

    def caltra(self): 	
	a=1
	global Train_path
	self.label_8.setText("Please wait..Training database!! ")
	t1=threading.Thread(target=train.Train,args=(Train_path,))     		
	t1.start()	
	self.onStart()
	self.pushButton.setEnabled(False)
	self.pushButton_2.setEnabled(False)
	self.pushButton_3.setEnabled(False)	
	while(1):
		QtCore.QCoreApplication.processEvents() 			
		if(t1.isAlive()==0):
			self.onFinished()
			self.label_8.setText("Trained!! Choose Test Image.. ")	
			self.pushButton.setEnabled(True)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(True)
	
			break	
		else:
			self.onStart()
	#self.label_5.setText("Trained!!!")

    def onStart(self): 
        self.progressBar.setRange(0,0)

    def onFinished(self):
        # Stop the pulsation
    	self.progressBar.setRange(0,1)
    	self.progressBar.setValue(1)

    def Browse2(self): 
        global Image_path           
	
	self.label_5.setText("")
	self.label_6.clear()      #  button event handler
        Image_path =tkFileDialog.askopenfilename()		
        self.label_2.setPixmap(QtGui.QPixmap(Image_path))
	self.label_3.setPixmap(QtGui.QPixmap("default.jpg"))        
	self.lineEdit_3.setText(Image_path)
	
    def final(self):
        global Image_path,Train_path  
        path=test.Test(Image_path) 
        for i in range(1,path+1):
            path2=Train_path+"/"+str(i) 
	    QtCore.QCoreApplication.processEvents() 			
            self.label_3.setPixmap(QtGui.QPixmap(path2))
	    time.sleep(.1)
	self.label_5.setText("MATCH FOUND!")
	self.label_6.setPixmap(QtGui.QPixmap("Tick4.jpg"))        
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
