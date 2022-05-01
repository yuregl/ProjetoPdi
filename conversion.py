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

def correlacao(path_picture, mask_matrix, row_pivot, col_pivot, row_mask, col_mask, func):
  
  # essa função consiste na implementação da correlação 
  # não normalizada entre uma mascara (masc_matriz) MxN e
  # os três canais de cor uma imagem.

  picture = cv.imread(path_picture, 3)
  row_picture, col_picture, ch = picture.shape

  b_matrix, g_matrix, r_matrix = cv.split(picture)

  inc_row = row_mask - 1 
  inc_col = col_mask - 1

  counter = (row_mask * col_mask)

  print("counter: ", counter)

  r_matrix_ext, g_matrix_ext, b_matrix_ext = ut.craete_extended_matrix_rgb_pivot(r_matrix, g_matrix, b_matrix, inc_row, inc_col, row_pivot, col_pivot)
  r_matrix_correlacao, g_matrix_correlacao, b_matrix_correlacao = ut.create_rgb_matrixes(row_picture, col_picture)
  
  #Dimensões da imagem e da máscara.
  #print("row_picture:", row_picture, " col_picture: ", col_picture, " row_mask: ", row_mask, " col_mask: ", col_mask)

  mask_matrix_1d = np.array(mask_matrix).flatten()

  for i in range(row_picture):
    for j in range(col_picture):
      limit_row_mask = i + row_mask
      limit_col_mask = j + col_mask

      r_aux_1d = np.array(r_matrix_ext[i:limit_row_mask, j:limit_col_mask]).flatten()
      g_aux_1d = np.array(g_matrix_ext[i:limit_row_mask, j:limit_col_mask]).flatten()
      b_aux_1d = np.array(b_matrix_ext[i:limit_row_mask, j:limit_col_mask]).flatten()

      r_correlacao_aux = 0
      g_correlacao_aux = 0
      b_correlacao_aux = 0
      
      for k in range(counter):
        r_correlacao_aux = r_correlacao_aux + (r_aux_1d[k] * mask_matrix_1d[k])
        g_correlacao_aux = g_correlacao_aux + (g_aux_1d[k] * mask_matrix_1d[k])
        b_correlacao_aux = b_correlacao_aux + (b_aux_1d[k] * mask_matrix_1d[k])
        #print("r_correlacao: ",r_aux_1d[k] * masc_matriz_1d[k])

      r_matrix_correlacao[i][j] = int(r_correlacao_aux)
      g_matrix_correlacao[i][j] = int(g_correlacao_aux)
      b_matrix_correlacao[i][j] = int(b_correlacao_aux) 

  print("r_matrix_correlacao: ")
  print(r_matrix_correlacao)
  correlacao_picture = cv.merge((r_matrix_correlacao, g_matrix_correlacao, b_matrix_correlacao))
  
  ut.save_image(func, correlacao_picture)
  
  return correlacao_picture 