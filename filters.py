import utils as ut
import numpy as np
import conversion

save_path_folder = './assets/images/'

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
  
def media(r_matriz, g_matriz, b_matriz, masc_matriz, lin_pivo, lin_col):
  
  r_media, g_media, b_media = conversion.correlacao(r_matriz, g_matriz, b_matriz, masc_matriz, lin_pivo, lin_col)
  img_media = cv.merge(r_media, g_media, b_media)
  func = "media"
  name_path = '{}{}.jpg'.format(save_path_folder,func)
  ut.save_image(name_path, img_media)

#def sobel_v():


#def sobel_h():
  
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