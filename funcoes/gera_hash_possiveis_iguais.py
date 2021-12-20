import os
import ast
import json
import piexif
import numpy as np
import pandas as pd
import piexif.helper
import multiprocessing as mp

from PIL import Image
from multiprocessing import Pool
from funcoes.auxiliares import *
from imagededup.methods import PHash, DHash
from funcoes.configuracao import *
from funcoes.gera_hash_todos_imoveis import percorre_imovel

def gera_hash_possiveis_iguais(csv_path,path_fotos):
    """
        DOCUMENTAR
    """
    percorre_pastas(csv_path,path_fotos)

def percorre_pastas(csv_path,path_fotos):
    """
        DOCUMENTAR
    """
    df = pd.read_csv(csv_path)
    info = list(zip(df["Nome"],df["lista_iguais"]))
    # cria_processos(info,path_fotos)
    processos = cria_processos(info,path_fotos)
    inicia_processos(processos)


def cria_processos(info,path_fotos):
    # N_PROCESSOS = 1
    # imoveis_split = np.array_split(info,N_PROCESSOS)  
    # input_ = gera_inputs_pool_imovel(imoveis_split,path_fotos)
    # with Pool(processes=N_PROCESSOS) as pool:
    #     pool.starmap(percorre_candidados_iguais,input_)
    imoveis_split = np.array_split(info,N_PROCESSOS) 
    lista_p = []
    for i in range(N_PROCESSOS):
        processo = mp.Process(target=percorre_candidados_iguais, args=(imoveis_split[i],path_fotos))
        lista_p.append(processo)
    
    return lista_p

def inicia_processos(processos):
    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()    
        
def percorre_candidados_iguais(lista_para_comparar,path_fotos):
    for i,comparavel in enumerate(lista_para_comparar):
        para_comparar = ast.literal_eval(comparavel[1]) + [comparavel[0]]
        for imovel in para_comparar:
            nome_imovel,nome_pasta = imovel.split("-")
            path_imovel = os.path.join(path_fotos,os.path.join(nome_pasta,nome_imovel))
            percorre_imovel(path_imovel)

        if i%50 == 0: 
            print(os.getpid(),' ---> ', i, '-', len(lista_para_comparar))
