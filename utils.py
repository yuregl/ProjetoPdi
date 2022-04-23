from PIL import Image
import numpy as np
import cv2 as cv

def save_image(url ,img):
	im = Image.fromarray(img)
	# im.show()
	im.save(url)

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

def create_extended_matrix_y(y_matrix, i_matrix, q_matrix, inc_row ,inc_col):
	row = y_matrix.shape[0]
	col = y_matrix.shape[1]	

	y_extended = np.zeros((row + inc_row * 2, col + inc_col * 2), dtype=np.uint8)
	i_extended = np.zeros((row + inc_row * 2, col + inc_col * 2), dtype=np.uint8)
	q_extended = np.zeros((row + inc_row * 2, col + inc_col * 2), dtype=np.uint8)

	for i in range(row):
		for j in range(col):
			y_extended[i + inc_row, j + inc_col] = y_matrix[i, j]
			i_extended[i + inc_row, j + inc_col] = i_matrix[i, j]
			q_extended[i + inc_row, j + inc_col] = q_matrix[i, j]

	return y_extended, i_extended, q_extended
