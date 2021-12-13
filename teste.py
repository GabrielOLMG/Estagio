import pandas as pd
import os
'''
    Funções/Classes de teste
'''
#--------------------------------------------- Faz um csv com todos os imoveis, para simular.

def percorre_pastas(PATH, CSV_PATH):
    pastas = os.listdir(PATH)
    nomes_todos = []
    paths_todos = []
    pasta_todos = []
    for pasta in pastas:
        # if(pasta == "0"): continue
        path_pasta = os.path.join(PATH, pasta)
        nomes,paths = percorre_imoveis(path_pasta)
        nomes_todos.extend(nomes)
        paths_todos.extend(paths)
        pasta_todos.extend([pasta]*len(nomes))
        
        break
    cria_csv(nomes_todos,pasta_todos, CSV_PATH)

def percorre_imoveis(PATH):
    imoveis = os.listdir(PATH)
    nomes = []
    paths = []
    for imovel in imoveis:
        nome = imovel
        path = os.path.join(PATH,imovel)
        nomes.append(nome)
        paths.append(path)
    return nomes,paths

def cria_csv(NOMES,PASTAS,CSV_PATH):
    dicionario = {"cfr":NOMES, "ecd" :PASTAS}
    df = pd.DataFrame(dicionario)
    df.to_csv(CSV_PATH,index=False)


if __name__ == '__main__':
    path_ = "FOTOS"
    path_csv = "CSV_FILES/imoveis.csv"
    percorre_pastas(path_,path_csv)