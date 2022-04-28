import conversion
import filters
import utils as ut

if __name__ == "__main__":
  file = "./assets/Woman.png"
  file_txt  = './assets/input3.txt' 
  while(True): 
    selectInput = input(
        "\t+---+-------------------------------------------------------+\n"
        +"\t|   |           Digite o numero da opção desejada           |\n"
        +"\t+---+-------------------------------------------------------+\n"
        +"\t| 1 | RGB-YIQ-RGB                                           |\n"
        +"\t| 2 | Negativo                                              |\n"
        +"\t| 3 | Correlação                                            |\n"
        +"\t| 4 | Mediana na banda Y                                    |\n"
        +"\t| 0 | Sair                                                  |\n"
        +"\t+---+-------------------------------------------------------+\n")

    if(selectInput == '1'):
      rgb_yiq_rgb = conversion.rgb_yiq_rgb(file, 'RGB-YIQ-RGB')
    
    if(selectInput == '2'):
      negative = conversion.negative(file, 'NEGATIVO')
      y_matrix, i_matrix, q_matrix = conversion.convert_to_yiq(file)
      conversion.negative_in_y(y_matrix, i_matrix, q_matrix,'NEGATIVO_IN_Y')

    if(selectInput == '3'):
      values = ut.read_file(file_txt)
      print(values)

    if(selectInput == '4'):
      row = int(input("Tamanaho das linhas: "))
      column = int(input("Tamanho das colunas: "))

      if(row % 2 == 0 or column % 2 == 0):
        print('Valores inválidos')
        continue
      
      y_matrix, i_matrix, q_matrix = conversion.convert_to_yiq(file)
      filters.median_in_y(y_matrix, i_matrix, q_matrix, row, column ,'MEDIANA_EM_Y')
    if(selectInput == '0'):
      break