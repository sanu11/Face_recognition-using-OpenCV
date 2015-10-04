import sys
import Tkinter
import tkFileDialog
from PyQt4 import QtCore, QtGui, uic 
import os
import Image
import numpy as np
import cv2
global Image_path,Train_path
global m,et,wt_matrix
form_class = uic.loadUiType("example.ui")[0]                 # Load the UI
class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Browse)  # Bind the event handlers
        self.pushButton_3.clicked.connect(self.Browse2)  #   to the buttons
        self.pushButton_2.clicked.connect(self.final)
	self.pushButton_4.clicked.connect(self.caltra)        
	self.label_2.setPixmap(QtGui.QPixmap("default.jpg"))
        self.label_3.setPixmap(QtGui.QPixmap("default.jpg"))
	self.progressBar.setValue(0)
	
    def Browse(self): 
        global Train_path
	root = Tkinter.Tk()
	root.withdraw()                 # button event handler
	Train_path=tkFileDialog.askdirectory()		
	#filedialog= QtGui.QFileDialog()   	
	#Train_path=str(filedialog.getExistingDirectory(self,"Select Train Directory"))
	x=Train_path.split('/')
	print Train_path
    	l=len(x)	
	self.lineEdit.setText(x[l-1])
    	
    def caltra(self): 	
	global Train_path
	self.label_5.setText("Please wait..Training database!! ")
	self.onStart()        	
        self.Train(Train_path)	 
        self.onFinished()
	self.label_5.setText("Trained!!!")

    def onStart(self): 
        self.progressBar.setRange(0,0)

    def onFinished(self):
        # Stop the pulsation
    	self.progressBar.setRange(0,1)
    	self.progressBar.setValue(1)

    def Browse2(self): 
        global Image_path                 #  button event handler
        Image_path = str(QtGui.QFileDialog(self).getOpenFileName())
        self.label_2.setPixmap(QtGui.QPixmap(Image_path))
	self.label_3.setPixmap(QtGui.QPixmap("default.jpg"))        
	self.lineEdit_2.setText(Image_path)

    def final(self):
        global Image_path
        path=self.Test(Image_path) 
        for i in range(0,path+1):
            path2=Train_path+"/"+str(i) 
            #os.sleep(10)
            self.label_3.setPixmap(QtGui.QPixmap(path2))
    def Train(self,path):
	QtCore.QCoreApplication.processEvents() 
	global m,et,wt_matrix
	im = Image.open(path +"/1")
	m= im.size[0]													#dimensions of image 
	n=im.size[1]	
	print m,n
	L=[]
	lst = os.listdir(path) 				#dir is path of Train database
	l = len(lst)																		#read image and append it as a column to L
	for i in range(1,l+1):
		QtCore.QCoreApplication.processEvents() 	
		path2=path + "/"+str(i)#".jpg"
		im = Image.open(path2)
		im2=im.save("try.jpg")
		QtCore.QCoreApplication.processEvents() 		
		data=cv2.imread("try.jpg",0)
		data=data.reshape(m*n,1)
		data=np.array(data[:,0])
		L.append(data)

	QtCore.QCoreApplication.processEvents() 	
	a=np.asarray(L)												 #convert list to np.array 
	ImageVector=a.T 											 #Transpose since list is appended as a row ..we need it as a column.

	#----------------Eigen_faces------------------------------------

	m=np.mean(ImageVector,axis=1)								 #mean about columns (axis=1 gives mean about column)

	A=ImageVector-m[:,None]    							         #Difference matrix(Unique features)
	At=A.T 														 #Transpose of Difference matrix				
	covar=At.dot(A)												 #covariance = A transpose into A

	eival, eivec = cv2.eigen(covar, computeEigenvectors=True)[1:] #eigen values and vectors of covariance matrix

	pri=[]
	QtCore.QCoreApplication.processEvents() 		
	column_count=len(ImageVector[0])

	t=0;

	for i in range(0,column_count):      						 #ignore eigen vectors less than threshold
		QtCore.QCoreApplication.processEvents() 			
		if(eival[i]>1):
			pri.append(eivec[:,i])
			t=t+1	
	QtCore.QCoreApplication.processEvents() 		
	prim=np.asarray(pri)				 						 #convert to np.array as pri is list
	primary=prim.transpose()

	Eiganfaces=A.dot(primary)			 					   	 #to get original dataset in terms of eigen vectors

	#-------------------Recognition---------------------------------
	QtCore.QCoreApplication.processEvents() 	
	wt=[]
	counter=len(Eiganfaces[0])									#number of eigen vectors in eigenfaces.

	et=Eiganfaces.transpose()
	
	for i in range(0,counter):
		QtCore.QCoreApplication.processEvents() 		
		wt.append(et.dot(A[:,i]))								#multiply a image column(A(:,i)) with every vector in (Eigenfaces)
	QtCore.QCoreApplication.processEvents() 		
	wt1=np.asarray(wt)
	wt_matrix=wt1.transpose()
	print "Trained!"
	return et,wt_matrix
	
    def Test(self,name1):
	QtCore.QCoreApplication.processEvents() 	
	global m,wt_matrix,et
	et=train.et
	wt_matrix=train.wt_matrix
						#test image
	img = Image.open(name1).convert('L')
	img.save('try2.jpg')
	test=cv2.imread('try2.jpg',0)							
	test1=test.ravel()
	diff_image=(test1)-(m)
	test2=et.dot(diff_image)

	#-----calculating Euclidian distance--------
		
	Euc=[]
	cnt=len(wt_matrix[0])

	for i in range(0,cnt):
		QtCore.QCoreApplication.processEvents() 		
		temp=(np.linalg.norm(test2-wt_matrix[:,i]))**2     #norm:-adds square of every row and takes square_root of the end sum
		Euc.append(temp)
	QtCore.QCoreApplication.processEvents() 		
	Euc_dis=np.asarray(Euc)
	index=np.where(Euc_dis==Euc_dis.min())				   #getting min distance's index ..i.e most perfectly matched image
	
	k=Euc_dis.argmin()
	k=k+1
	print k
	return k
#---------------------END-------------------------
	



app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
