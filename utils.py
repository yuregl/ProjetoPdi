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

def craete_extended_matrix_rgb_pivot(r_matrix, g_matrix, b_matrix, inc_row, inc_col, row_pivot, col_pivot):

	row = r_matrix.shape[0]
	col = r_matrix.shape[1]	

	r_matrix_ext = np.zeros((row + inc_row, col + inc_col), dtype=np.uint8)
	g_matrix_ext = np.zeros((row + inc_row, col + inc_col), dtype=np.uint8)
	b_matrix_ext = np.zeros((row + inc_row, col + inc_col), dtype=np.uint8)

	for i in range (row):
		for j in range (col):
			r_matrix_ext[i + row_pivot, j + col_pivot] = r_matrix[i, j]
			g_matrix_ext[i + row_pivot, j + col_pivot] = g_matrix[i, j]
			b_matrix_ext[i + row_pivot, j + col_pivot] = b_matrix[i, j]
	
	return r_matrix_ext, g_matrix_ext, b_matrix_ext

def expansao_de_histograma(r_matrix, g_matrix, b_matrix):

	l = 255

	row = r_matrix.shape[0]
	col = r_matrix.shape[1]

	r_min = np.min(r_matrix)
	r_max = np.max(r_matrix)
	g_min = np.min(g_matrix)
	g_max = np.max(g_matrix)
	b_min = np.min(b_matrix)
	b_max = np.max(b_matrix)

	r_matrix_exp_his,g_matrix_exp_his, b_matrix_exp_his = create_rgb_matrixes(row, col)

	for i in range(row):
		for j in range(col):
			r_matrix_exp_his[i, j] = (((r_matrix[i, j] - r_min) * l ) // (r_max - r_min))
			g_matrix_exp_his[i, j] = (((g_matrix[i, j] - g_min) * l ) // (g_max - g_min))
			b_matrix_exp_his[i, j] = (((b_matrix[i, j] - b_min) * l ) // (b_max - b_min))

	return r_matrix_exp_his,g_matrix_exp_his, b_matrix_exp_his


def read_file(path):
	all_file = open(path, "r")
	read_lines = all_file.readlines()
	offset=int(read_lines[0].split()[1])
	row=int(read_lines[1].split()[1])
	col=int(read_lines[2].split()[1])
	line_pivot = 5 + 2*row
	pivot_row = int(read_lines[line_pivot].split()[1])
	pivot_col = int(read_lines[line_pivot].split()[2])

	mask_sobel_horizontal = []
	mask_sobel_vertical = []
	mask_media = []

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
	
	begin_line_mask_media = 7 + 2*row 
	end_line_mask_media = begin_line_mask_media + row

	for row_mask in range (begin_line_mask_media, end_line_mask_media):
		aux_arr = []
		for col_mask in range (col):
			arr_line = read_lines[row_mask].split()
			aux_arr.append(float(arr_line[col_mask]))
		mask_media.append(aux_arr)

	return offset, row, col, mask_sobel_horizontal, mask_sobel_vertical, mask_media, pivot_row, pivot_col


