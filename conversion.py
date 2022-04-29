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

def correlacao(r_matriz, g_matriz, b_matriz, masc_matriz, lin_pivo, col_pivo):

  # essa função consiste na na implementação da correlação 
  # não normalizada entre uma mascara (mask_matrix) MxN e
  # os três canais de cor uma imagem.

  # dimensões da imagem e da mascara.
  lin_img, col_img = r_matriz.shape()
  lin_masc, col_masc = masc_matriz.shape()

  inc_lin = lin_masc - 1;
  inc_col = col_masc - 1;

  contador_pi = lin_masc*col_masc

  #criando uma imagem para cada canal com extensão por zero.
  r_matriz_ext, g_matriz_ext, b_matriz_ext = ut.cria_matrizes_extendidas_pivo(r_matriz, g_matriz, b_matriz, inc_lin, inc_col, lin_pivo, col_pivo)

  #criando uma imagem de saída para cada canal de cor.
  r_correlacao_matriz, g_correlacao_matriz, b_correlacao_matriz = ut.create_rgb_matrixes(lin_img, col_img)

  # criando uma cópia da matriz da mascara recolhida em uma
  # dimensão, para facilitar o cálculo do produto interno.
  masc_matriz_1d = masc_matriz.flatten()
  
  for i in range(lin_img):
    for j in range(col_img):
      limite_lin_masc = i + lin_masc
      limite_col_masc = j + col_masc

      r_aux_1d = np.array(r_matriz_ext[i:limite_lin_masc, j:limite_col_masc]).flatten()
      g_aux_1d = np.array(g_matriz_ext[i:limite_lin_masc, j:limite_col_masc]).flatten()
      b_aux_1d = np.array(b_matriz_ext[i:limite_lin_masc, j:limite_col_masc]).flatten()

      #produto interno
      for k in range(contador_pi):
        r_correlacao_matriz[i,j] = r_correlacao_matriz[i,j] + (r_aux_1d[k]*masc_matriz_1d[k])
        g_correlacao_matriz[i,j] = g_correlacao_matriz[i,j] + (g_aux_1d[k]*masc_matriz_1d[k])
        b_correlacao_matriz[i,j] = b_correlacao_matriz[i,j] + (b_aux_1d[k]*masc_matriz_1d[k])
      
      r_correlacao_matriz[i,j] = int(r_correlacao_matriz[i,j])
      g_correlacao_matriz[i,j] = int(g_correlacao_matriz[i,j])
      b_correlacao_matriz[i,j] = int(b_correlacao_matriz[i,j]) 

  return r_correlacao_matriz, g_correlacao_matriz, b_correlacao_matriz