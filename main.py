import conversion

if __name__ == "__main__":
  file = "./assets/Woman.png"
  while(True): 
    selectInput = input(
        "\t+---+-------------------------------------------------------+\n"
        +"\t|   |           Digite o numero da opção desejada           |\n"
        +"\t+---+-------------------------------------------------------+\n"
        +"\t| 1 | RGB-YIQ-RGB                                           |\n"
        +"\t| 2 | Negativo                                              |\n"
        +"\t| 0 | Sair                                                  |\n"
        +"\t+---+-------------------------------------------------------+\n")

    if(selectInput == '1'):
      rgb_yiq_rgb = conversion.rgb_yiq_rgb(file)
    
    if(selectInput == '2'):
      negative = conversion.negative(file)
    
    if(selectInput == '0'):
      break