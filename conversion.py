import cv2 as cv
import numpy as np
import utils as ut

save_path_folder = './assets/images/'

def convert_to_yiq(path):
  img = cv.imread(path, 3)
  row, col, ch = img.shape
  blue, green, red = cv.split(img)

  y_matrix, i_matrix, q_matrix = ut.create_yiq_matrixes(row, col)

  for i in range(row):
    for j in range(col):
      r = red[i, j]
      g = green[i, j]
      b = blue[i, j]
      # RGB to YIQ
      y_matrix[i, j] = (0.299 * r) + (0.587 * g) + (0.114 * b)
      i_matrix[i, j] = (0.596 * r) - (0.274 * g) - (0.322 * b)
      q_matrix[i, j] = (0.211 * r) - (0.523 * g) + (0.312 * b)

  return y_matrix, i_matrix, q_matrix

def convert_to_rgb(y_matrix, i_matrix, q_matrix, func):
  row = y_matrix.shape[0]
  col = y_matrix.shape[1]

  r_matrix, g_matrix, b_matrix = ut.create_rgb_matrixes(row, col)

  for x in range(0, row):
    for j in range(0, col):
      y = y_matrix[x, j]
      i = i_matrix[x, j]
      q = q_matrix[x, j]
      # YIQ to RGB
      r_matrix[x, j] = int(min(max((1.000 * y) + (0.956 * i) + (0.621 * q),0),255))
      g_matrix[x, j] = int(min(max((1.000 * y) - (0.272 * i) - (0.647 * q),0),255))
      b_matrix[x, j] = int(min(max((1.000 * y) - (1.106 * i) + (1.703 * q),0),255))

  rgb_img = cv.merge([ r_matrix, g_matrix, b_matrix ])
  name_path = '{}{}.jpg'.format(save_path_folder,func)
  ut.save_image(name_path ,rgb_img)

def rgb_yiq_rgb(path, func):
  y_matrix, i_matrix, q_matrix = convert_to_yiq(path)
  convert_to_rgb(y_matrix, i_matrix, q_matrix, func)

def negative(path, func):
  img = cv.imread(path,3)
  row, col, ch = img.shape

  blue, green, red = cv.split(img)
  r_matrix, g_matrix, b_matrix = ut.create_rgb_matrixes(row, col)

  for i in range(row):
    for j in range(col):
      r_matrix[i, j] = 255 - red[i, j]
      g_matrix[i, j] = 255 - green[i, j]
      b_matrix[i, j] = 255 - blue[i, j]

  negativeImage = cv.merge([r_matrix, g_matrix, b_matrix])
  name_path = '{}{}.jpg'.format(save_path_folder,func)
  ut.save_image(name_path,negativeImage)

def negative_in_y(y_matrix, i_matrix, q_matrix, func):
  row = y_matrix.shape[0]
  col = y_matrix.shape[1]

  y_matrix_negative, value_i, value_q = ut.create_yiq_matrixes(row, col)

  for i in range(row):
    for j in range(col):
      y_matrix_negative[i, j] = 255 - y_matrix[i, j]
  
  convert_to_rgb(y_matrix_negative, i_matrix, q_matrix, func)
