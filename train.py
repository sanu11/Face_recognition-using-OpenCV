import numpy as np
import cv2
import Image
import os
global m,et,wt_matrix
#--------------Create database---------------------------------
def Train(path):
	global m,et,wt_matrix
	im = Image.open(path+"/1")
	m= im.size[0]													#dimensions of image 
	n=im.size[1]	
	print m,n
	L=[]
	lst = os.listdir(path) 				#dir is path of Train database
	l = len(lst)																		#read image and append it as a column to L
	for i in range(1,l+1):
		path2=path + "/"+str(i)#".jpg"
		im = Image.open(path2)
		im2=im.save("try.jpg")
		data=cv2.imread("try.jpg",0)
		data=data.reshape(m*n,1)
		data=np.array(data[:,0])
		L.append(data)

	a=np.asarray(L)												 #convert list to np.array 
	ImageVector=a.T 											 #Transpose since list is appended as a row ..we need it as a column.

	#----------------Eigen_faces------------------------------------

	m=np.mean(ImageVector,axis=1)								 #mean about columns (axis=1 gives mean about column)

	A=ImageVector-m[:,None]    							         #Difference matrix(Unique features)
	At=A.T 														 #Transpose of Difference matrix				
	covar=At.dot(A)												 #covariance = A transpose into A

	eival, eivec = cv2.eigen(covar, computeEigenvectors=True)[1:] #eigen values and vectors of covariance matrix

	pri=[]

	column_count=len(ImageVector[0])

	t=0;

	for i in range(0,column_count):      						 #ignore eigen vectors less than threshold
		if(eival[i]>1):
			pri.append(eivec[:,i])
			t=t+1	

	prim=np.asarray(pri)				 						 #convert to np.array as pri is list
	primary=prim.transpose()

	Eiganfaces=A.dot(primary)			 					   	 #to get original dataset in terms of eigen vectors

	#-------------------Recognition---------------------------------

	wt=[]
	counter=len(Eiganfaces[0])									#number of eigen vectors in eigenfaces.

	et=Eiganfaces.transpose()

	for i in range(0,counter):
		wt.append(et.dot(A[:,i]))								#multiply a image column(A(:,i)) with every vector in (Eigenfaces)

	wt1=np.asarray(wt)
	wt_matrix=wt1.transpose()
	print "Trained!"
	return et,wt_matrix
