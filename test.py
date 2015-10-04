import numpy as np
import cv2
import Image
import os
import train
def Test(name1):
	m=train.m
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
		temp=(np.linalg.norm(test2-wt_matrix[:,i]))**2     #norm:-adds square of every row and takes square_root of the end sum
		Euc.append(temp)

	Euc_dis=np.asarray(Euc)
	index=np.where(Euc_dis==Euc_dis.min())				   #getting min distance's index ..i.e most perfectly matched image
	
	k=Euc_dis.argmin()
	k=k+1
	print k
	return k
#---------------------END-------------------------
	
