import models

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, metrics, datasets
from sklearn.utils import Bunch
from sklearn.model_selection import GridSearchCV, train_test_split

from skimage.io import imread
from skimage.transform import resize
from pickle import dump
from pickle import load



def get_model_from_image(capture):


	clf = load(open('model.pkl', 'rb'))

	ret, image = capture.read()

	img_test = image
	img_resized_test = resize(img_test, (64, 64), anti_aliasing=True, mode='reflect')
	img_resized_test = img_resized_test.flatten().reshape(1, -1)
	print(img_resized_test)

	y_pred_test = clf.predict(img_resized_test)
	print("Detected Model: ", y_pred_test)

	if y_pred_test[0] == 0:
		print("Wheat Flour Bread")
		model = models.white_bread_model_1
	else:
		print("Whole Grain Bread")
		model = models.brown_bread_model
	return model
