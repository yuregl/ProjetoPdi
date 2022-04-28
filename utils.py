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

def read_file(path):
	all_file = open(path, "r")
	read_lines = all_file.readlines()
	offset=int(read_lines[0].split()[1])
	row=int(read_lines[1].split()[1])
	col=int(read_lines[2].split()[1])
	line_pivo = 5 + 2*row
	pivo_row = int(read_lines[line_pivo].split()[1])
	pivo_col = int(read_lines[line_pivo].split()[2])

	mask_sobel_horizontal = []
	mask_sobel_vertical = []

	for row_mask in range(4, row+4):
		aux_arr = []
		for col_mask in range(col):
			arr_line = read_lines[row_mask].split()
			aux_arr.append(int(arr_line[col_mask]))
		mask_sobel_horizontal.append(aux_arr)

	begin_line_mask_vertical = 5 + row
	end_line_mask_vertical = begin_line_mask_vertical+row

	for row_mask in range(begin_line_mask_vertical, end_line_mask_vertical):
		aux_arr = []
		for col_mask in range(col):
			arr_line = read_lines[row_mask].split()
			aux_arr.append(int(arr_line[col_mask]))
		mask_sobel_vertical.append(aux_arr)
	

	return offset, row, col, mask_sobel_horizontal, mask_sobel_vertical, pivo_row, pivo_col


