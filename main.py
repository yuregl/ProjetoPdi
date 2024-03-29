import conversion
import filters
import advancedFunctions as af
import utils as ut

if __name__ == "__main__":
  file = "./assets/Woman.png"
  file_txt  = './assets/input3.txt' 
  file_woman_eye = './assets/Woman_eye.png'
  while(True): 
    selectInput = input(
        "\t+---+-------------------------------------------------------+\n"
        +"\t|   |           Digite o numero da opção desejada           |\n"
        +"\t+---+-------------------------------------------------------+\n"
        +"\t| 1 | RGB-YIQ-RGB                                           |\n"
        +"\t| 2 | Negativo                                              |\n"
        +"\t| 3 | Correlação                                            |\n"
        +"\t| 4 | Mediana na banda Y                                    |\n"
        +"\t| 5 | Correlação avançada                                   |\n"
        +"\t| 0 | Sair                                                  |\n"
        +"\t+---+-------------------------------------------------------+\n")

    if(selectInput == '1'):
      rgb_yiq_rgb = conversion.rgb_yiq_rgb(file, 'RGB-YIQ-RGB')
    
    if(selectInput == '2'):
      negative = conversion.negative(file, 'NEGATIVO')
      y_matrix, i_matrix, q_matrix = conversion.convert_to_yiq(file)
      conversion.negative_in_y(y_matrix, i_matrix, q_matrix,'NEGATIVO_IN_Y')

    if(selectInput == '3'):
      offset, row, col, mask_sobel_horizontal, mask_sobel_vertical, mask_media, pivot_row, pivot_col = ut.read_file(file_txt)  

      filters.media(file, mask_media, pivot_row, pivot_col, row, col, offset)
      filters.sobel(file, mask_sobel_horizontal, mask_sobel_vertical, pivot_row, pivot_col, row, col, offset)

    if(selectInput == '4'):
      row = int(input("Tamanaho das linhas: "))
      column = int(input("Tamanho das colunas: "))

      if(row % 2 == 0 or column % 2 == 0):
        print('Valores inválidos')
        continue
      
      y_matrix, i_matrix, q_matrix = conversion.convert_to_yiq(file)
      filters.median_in_y(y_matrix, i_matrix, q_matrix, row, column ,'MEDIANA_EM_Y')
    
    if(selectInput == '5'):
      path_fist_correlation = af.avanced_correlation(file, file_woman_eye, 'FIRSTCORRELATION')
      af.avanced_correlation(path_fist_correlation, file_woman_eye, 'SECONDCORRELATION')

    if(selectInput == '0'):
      break