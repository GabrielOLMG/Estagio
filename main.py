
import time
from funcoes.gera_hash_imoveis import gera_hash_imoveis
from funcoes.compara_imoveis import compara_imoveis


if __name__ == "__main__":
    PATH_FOTOS = "FOTOS"
    CSV_PATH = "CSV_FILES\dados_gabriel.csv"
    CSV_PATH_TESTE = "CSV_FILES/imoveis.csv"
    '''
    Passo 1 
        - gera as hash
        - verifica se  tem imagem repetida dentro e deleta as que estão repetidas
    '''
    # start = time.time()
    # gera_hash_imoveis(CSV_PATH_TESTE,PATH_FOTOS) # ja feito
    # stop = time.time()
    # print(f"<<The time of the run: {stop - start}>>")

    print("---------------------------------------------------------------------------------------------------------------")
    '''
    # Passo 2 - Compara imoveis
        - compara imovel com imove
        - se dois imoveis são iguas então deleta um deles
            - Caso 2 imoveis seja iguais e um imovel tenha imagens que o outro não tenha, 
                então devo copiar os arquivos para o que vai ficar.
            - a principio não devo apagar, devo so colocar em um csv para dps verificar
        - se dois imoveis são indeterminados, devo criar um csv contendo essa informação (imovel1 imovel2)

    '''
    start = time.time()
    compara_imoveis(CSV_PATH_TESTE,PATH_FOTOS)
    stop = time.time()
    print(f"<<The time of the run: {stop - start}>>")
