from PIL import Image
import numpy as np
import cv2 as cv

def show_image(method, img):
	im = Image.fromarray(img)
	im.show()

def create_yiq_matrixes(row, col):
	y_matrix = np.zeros((row, col))
	i_matrix = np.zeros((row, col))
	q_matrix = np.zeros((row, col))
	return y_matrix, i_matrix, q_matrix

def create_rgb_matrixes(row, col):
	r_matrix = np.zeros((row, col), dtype=np.uint8)
	g_matrix = np.zeros((row, col), dtype=np.uint8)
	b_matrix = np.zeros((row, col), dtype=np.uint8)

	return r_matrix, g_matrix, b_matrix
