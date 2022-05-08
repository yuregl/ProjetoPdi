from PIL import Image
import cv2 as cv
from matplotlib import pyplot as plt
import utils as ut

def avanced_correlation(path_image, path_compare, path_save):
  img = cv.imread(path_image, 0)
  template = cv.imread(path_compare, 0)
  row_template, col_template = template.shape[::-1]

  res = cv.matchTemplate(img,template,eval('cv.TM_CCORR_NORMED'))
  min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
  
  top_left = max_loc
  bottom_right = (top_left[0] + row_template, top_left[1] + col_template)

  new_image = ''

  if(path_save == 'FIRSTCORRELATION'):
    new_image = cv.rectangle(img,top_left, bottom_right, 0, -1)
  else:
    new_image = cv.rectangle(img,top_left, bottom_right, 255, 2)

  path_new_image = './assets/images/{}.png'.format(path_save)
  ut.save_image(path_new_image, new_image)

  return path_new_image