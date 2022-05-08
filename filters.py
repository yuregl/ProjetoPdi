import utils as ut
import numpy as np
import conversion
import cv2 as cv


def median_in_y(y_matrix, i_matrix, q_matrix, row_mask, col_mask, func):
  row_image = y_matrix.shape[0]
  col_image = y_matrix.shape[1]

  inc_row = row_mask // 2
  inc_col = col_mask // 2
  y_ext, i_ext, q_ext = ut.create_extended_matrix_y(y_matrix, i_matrix, q_matrix, inc_row, inc_col)
  y_median_matrix, i_median_matrix, q_median_matrix = ut.create_yiq_matrixes(row_image, col_image)

  # conversion.convert_to_rgb(y_matrix, i_matrix, q_matrix, func)

  for i in range(row_image):
    for j in range(col_image):
      limit_mask_row = i+row_mask
      limit_mask_col = j+col_mask
      y_aux = np.sort(np.array(y_ext[i:limit_mask_row, j:limit_mask_col]).flatten())
      index = y_aux.shape[0] // 2
      y_median_matrix[i, j] = y_aux[index]

  conversion.convert_to_rgb(y_median_matrix, i_matrix, q_matrix, func)

def media(path_picture, mask_matrix, row_pivot, col_pivot, row_mask, col_mask, offset):

  func = "./assets/images/MEDIA.jpg"
  r_matrix_correlacao, g_matrix_correlacao, b_matrix_correlacao = conversion.correlacao(path_picture, mask_matrix, row_pivot, col_pivot, row_mask, col_mask, offset)
  
  correlacao_picture = cv.merge((r_matrix_correlacao, g_matrix_correlacao, b_matrix_correlacao))
  
  ut.save_image(func, correlacao_picture)

def sobel(path_picture, mask_sobel_horizontal, mask_sobel_vertical, row_pivot, col_pivot, row_mask, col_mask, offset ):
  print("Iniciando etapa da correlacao")
  
  r_matrix_sh, g_matrix_sh, b_matrix_sh = conversion.correlacao(path_picture, mask_sobel_horizontal, row_pivot, col_pivot, row_mask, col_mask, offset)
  r_matrix_sv, g_matrix_sv, b_matrix_sv = conversion.correlacao(path_picture, mask_sobel_vertical, row_pivot, col_pivot, row_mask, col_mask, offset)
  
  print("Iniciando etapa da expansao de histograma")

  r_matrix_sh_exph, g_matrix_sh_exph, b_matrix_sh_exph = ut.expansao_de_histograma(r_matrix_sh, g_matrix_sh, b_matrix_sh)
  r_matrix_sv_exph, g_matrix_sv_exph, b_matrix_sv_exph = ut.expansao_de_histograma(r_matrix_sv, g_matrix_sv, b_matrix_sv)

  print("etapa de expansao de histograma terminada, iniciando etapa da mesclagem dos canais para formacao da imagem")

  
  sobel_horizontal_picture = cv.merge((r_matrix_sh_exph, g_matrix_sh_exph, b_matrix_sh_exph))
  sobel_vertical_picture = cv.merge((r_matrix_sv_exph, g_matrix_sv_exph, b_matrix_sv_exph))

 

  ut.save_image("./assets/images/SOBEL_HORIZONTAL.jpg", sobel_horizontal_picture)
  ut.save_image("./assets/images/SOBEL_VERTICAL.jpg", sobel_vertical_picture)


# def median_in_y(y_matrix, i_matrix, q_matrix, row_mask, col_mask, func):
#   row_image = y_matrix.shape[0]
#   col_image = y_matrix.shape[1]

#   inc_row = row_mask // 2
#   inc_col = col_mask // 2
#   y_ext, i_ext, q_ext = ut.create_extended_matrix_y(y_matrix, i_matrix, q_matrix, inc_row, inc_col)
#   y_median_matrix, i_median_matrix, q_median_matrix = ut.create_yiq_matrixes(row_image, col_image)

#   # conversion.convert_to_rgb(y_matrix, i_matrix, q_matrix, func)

#   for i in range(row_image):
#     for j in range(col_image):
#       limit_mask_row = i+row_mask
#       limit_mask_col = j+col_mask
#       y_aux = np.sort(np.array(y_ext[i:limit_mask_row, j:limit_mask_col]).flatten())
#       i_aux = np.sort(np.array(i_ext[i:limit_mask_row, j:limit_mask_col]).flatten())
#       q_aux = np.sort(np.array(q_ext[i:limit_mask_row, j:limit_mask_col]).flatten())
#       index = y_aux.shape[0] // 2
#       y_median_matrix[i, j] = y_aux[index]
#       i_median_matrix[i, j] = i_aux[index]
#       q_median_matrix[i, j] = q_aux[index]

#   conversion.convert_to_rgb(y_median_matrix, i_median_matrix, q_median_matrix, func)