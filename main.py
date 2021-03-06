
import time
from funcoes.acha_duplicadas_csv import acha_duplicadas_csv
from funcoes.gera_hash_todos_imoveis import gera_hash_todos_imoveis
from funcoes.gera_hash_possiveis_iguais import gera_hash_possiveis_iguais
from funcoes.compara_imoveis import compara_imoveis



if __name__ == "__main__":
    CSV_PATH_METADADO_TESTE = "CSV_FILES\\teste.csv"
    CSV_PATH_TESTE = "CSV_POSSIVEIS_IGUAIS\possiveis_iguais.csv"

    PATH_FOTOS = "FOTOS"
    CSV_PATH_METADADO = "CSV_FILES\dados_gabriel.csv"
    CSV_PATH_OUTPUT = "CSV_OUTPUT/"
    CSV_PATH_POSSIVEIS_IGUAIS = "CSV_POSSIVEIS_IGUAIS/"

    
    '''
    Passo 1
        - Dado o csv com o metadata dos imoveis, irei criar um novo csv contendo as imagens iguais
    '''
    start = time.time()
    acha_duplicadas_csv(CSV_PATH_METADADO,CSV_PATH_POSSIVEIS_IGUAIS)
    stop = time.time()
    print(f"<<The time of the run: {stop - start}>>")

    '''
    Passo 2 
        - gera as hash
        - verifica se  tem imagem repetida dentro e deleta as que estão repetidas()
    '''
    #  start = time.time()
    # gera_hash_todos_imoveis(CSV_PATH_METADADO,PATH_FOTOS) # ja feito
    # stop = time.time()
    # print(f"<<The time of the run: {stop - start}>>")

    # ou

    #start = time.time()
    #gera_hash_possiveis_iguais(CSV_PATH_TESTE,PATH_FOTOS)
    #stop = time.time()
    #print(f"<<The time of the run: {stop - start}>>")
    #29 horas para finalizar
    print("---------------------------------------------------------------------------------------------------------------")
    '''
    # Passo 3 - Compara imoveis
        - compara imovel com imove
        - se dois imoveis são iguas então deleta um deles
            - Caso 2 imoveis seja iguais e um imovel tenha imagens que o outro não tenha, 
                então devo copiar os arquivos para o que vai ficar.
            - a principio não devo apagar, devo so colocar em um csv para dps verificar
        - se dois imoveis são indeterminados, devo criar um csv contendo essa informação (imovel1 imovel2)

    '''
    # start = time.time()
    # compara_imoveis(CSV_PATH_TESTE,PATH_FOTOS,CSV_PATH_OUTPUT)
    # stop = time.time()
    # print(f"<<The time of the run: {stop - start}>>")
