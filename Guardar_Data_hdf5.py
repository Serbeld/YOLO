# -*- coding: utf-8 -*-

from random import shuffle
import glob
import h5py
import numpy as np
import cv2
import time

shuffle_data = True  # shuffle the addresses before saving
hdf5_path = 'Colombian_cans.hdf5'  # file path for the created .hdf5 file
train_path = 'Train/*'  # the original data path

# get all the image paths
addrs = glob.glob(train_path)

print((addrs))
print()

# label the data
classes = []
labels = []
files = []
labelsNumbers = {}
indexlabel = 0

for subfolder in addrs:
	classes.append(subfolder)
	labelsNumbers[subfolder.split('_')[1]] = indexlabel
	indexlabel += 1
	files.append(glob.glob(subfolder+'/*'))

print(labelsNumbers)

addrs = [item for sublist in files for item in sublist]

print(len(addrs))
#print(addrs)

for f in addrs:
	l = f.split('_')[1] #Nombre de Clase

	if l == 'Golden':
		h = 0
	if l == 'DefectiveGolden':
		h = 1
	if l == 'DefectiveBlack':
		h = 2
	if l == 'Black':
		h = 3
	if l == 'Red':
		h = 4
	if l == 'DefectiveRed':
		h = 5

	#print(l)
	labels.append(h)

#print(titulos[0])
#print(labels[0])
#img = cv2.imread(addrs[0])
#cv2.imshow('Hola', img)
#cv2.waitKey(1000)

if shuffle_data:
	c = list(zip(addrs, labels))
	shuffle(c)
	# print(c)
	addrs, labels = zip(*c)

addrs = addrs[0:15000]
labels = labels[0:15000]

# Divide the data into 70% train, 15% validation, and 15% test
train_addrs = addrs[0:int(0.7 * len(addrs))]
train_labels = labels[0:int(0.7 * len(labels))]
val_addrs = addrs[int(0.7 * len(addrs)):int(0.85 * len(addrs))]
val_labels = labels[int(0.7 * len(addrs)):int(0.85 * len(addrs))]
test_addrs = addrs[int(0.85 * len(addrs)):]
test_labels = labels[int(0.85 * len(labels)):]

data_order = 'tf'  # 'th' for Theano, 'tf' for Tensorflow
if data_order == 'th':
	train_shape = (len(train_addrs), 3, 480, 640)
	val_shape = (len(val_addrs), 3, 480, 640)
	test_shape = (len(test_addrs), 3, 480, 640)

elif data_order == 'tf':
	train_shape = (len(train_addrs), 416, 416, 3)
	val_shape = (len(val_addrs), 416, 416, 3)
	test_shape = (len(test_addrs), 416, 416, 3)

# open a hdf5 file and create earrays
hdf5_file = h5py.File(hdf5_path, mode='w')
hdf5_file.create_dataset("train_img", train_shape, np.uint8)
hdf5_file.create_dataset("val_img", val_shape, np.uint8)
hdf5_file.create_dataset("test_img", test_shape, np.uint8)
#hdf5_file.create_dataset("train_mean", train_shape[1:], np.float32)
hdf5_file.create_dataset("train_labels", (len(train_addrs),), np.uint8)
hdf5_file["train_labels"][...] = train_labels
hdf5_file.create_dataset("val_labels", (len(val_addrs),), np.uint8)
hdf5_file["val_labels"][...] = val_labels
hdf5_file.create_dataset("test_labels", (len(test_addrs),), np.uint8)
hdf5_file["test_labels"][...] = test_labels

# a numpy array to save the mean of the images
#mean = np.zeros(train_shape[1:], np.float32)

# loop over train addresses
for i in range(len(train_addrs)):
	# print how many images are saved every 500 images
	if i % 500 == 0 and i > 1:
		print('Train data: ' + str(i) + '/' + str(len(train_addrs)))

	# cv2 load images as BGR, convert it to RGB
	addr = train_addrs[i]
	img = cv2.imread(addr)
	img = cv2.resize(img, (416,416), interpolation=cv2.INTER_CUBIC)
	#cv2.imshow('Hello', img)
	#cv2.waitKey(100)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2 load images as BGR, convert it to RGB
	try:
		img = img
		hdf5_file["train_img"][i, ...] = img[None]
		#mean += img / float(len(train_labels))
	except Exception as e:
		pass

# loop over validation addresses
for i in range(len(val_addrs)):
	# print how many images are saved every 500 images
	if i % 500 == 0 and i > 1:
		print('Validation data: ' + str(i) + '/' + str(len(val_addrs)))

	# cv2 load images as BGR, convert it to RGB
	addr = val_addrs[i]
	img = cv2.imread(addr)
	img = cv2.resize(img, (416,416), interpolation=cv2.INTER_CUBIC)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2 load images as BGR, convert it to RGB
	try:
		img = img
		hdf5_file["val_img"][i, ...] = img[None]
	except Exception as e:
		pass

# loop over test addresses
for i in range(len(test_addrs)):
	# print how many images are saved every 500 images
	if i % 500 == 0 and i > 1:
		print('Test data: ' + str(i) + '/' + str(len(test_addrs)))

	# cv2 load images as BGR, convert it to RGB
	addr = test_addrs[i]
	img = cv2.imread(addr)
	img = cv2.resize(img, (416,416), interpolation=cv2.INTER_CUBIC)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2 load images as BGR, convert it to RGB
	try:
		img = img
		hdf5_file["test_img"][i, ...] = img[None]
	except Exception as e:
		pass

# save the mean and close the hdf5 file
cv2.destroyAllWindows()
#hdf5_file["train_mean"][...] = mean
hdf5_file.close()
