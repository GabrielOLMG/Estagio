from logging import disable
import os
import numpy as np
import pandas as pd
from multiprocessing import Pool
from funcoes.auxiliares import *

from funcoes.configuracao import *

def compara_imoveis(CSV_PATH,FOTOS_PATH,CSV_PATH_OUTPUT):
    percorre_imoveis(CSV_PATH,FOTOS_PATH,CSV_PATH_OUTPUT)

def percorre_imoveis(CSV_PATH,FOTOS_PATH,CSV_PATH_OUTPUT):
    """
        DOCUMENTAR
    """
    df = pd.read_csv(CSV_PATH)
    info = list(zip(df["ecd"],df["cfr"]))
    for i in range(len(info)-1):
        imovel_atual = info[i]
        resto = info[i+1:]
        cria_processos(imovel_atual,resto,FOTOS_PATH,CSV_PATH_OUTPUT)

def cria_processos(imovel_atual,lista_imoveis,FOTOS_PATH,CSV_PATH_OUTPUT):
    imoveis_split = np.array_split(lista_imoveis,N_PROCESSOS)
    inputs_list = gera_inputs_pool_imovel(imovel_atual,imoveis_split,FOTOS_PATH)
    with Pool(processes=N_PROCESSOS) as pool:
        valores = pool.starmap(percorre_e_compara,inputs_list)
    flat_list = [item for sublist in valores for item in sublist]
    atualiza_csv(CSV_PATH_OUTPUT,flat_list) 

def percorre_e_compara(imovel_atual, imoveis,FOTOS_PATH):
    path_atual = os.path.join(FOTOS_PATH,os.path.join(str(imovel_atual[0]),str(imovel_atual[1])))
    img_imovel_atual = os.listdir(path_atual)
    resultados = []
    for i,imovel_a_comparar in enumerate(imoveis):
        if i%50 == 0: 
            print('PROCESSO ',os.getpid(),' ---> ', i, 'de', len(imoveis), 'feito')

        path_comparar = os.path.join(FOTOS_PATH, os.path.join(str(imovel_a_comparar[0]),str(imovel_a_comparar[1])))
        img_imovel_a_comparar = os.listdir(path_comparar)
        resultado = verifica_igualdade(path_atual,img_imovel_atual,path_comparar,img_imovel_a_comparar)
        resultados.append(resultado)
    
    return resultados


def verifica_igualdade(path_imovel_atual,img_imovel_atual,path_imovel_a_comparar,img_imovel_a_comparar):
    iguais = 0
    indeterminado = 0
    if len(img_imovel_atual) > len(img_imovel_a_comparar):
        maior = [path_imovel_atual,img_imovel_atual]
        menor = [path_imovel_a_comparar,img_imovel_a_comparar]
    else:
        maior = [path_imovel_a_comparar,img_imovel_a_comparar]
        menor = [path_imovel_atual,img_imovel_atual]

    for img_atual in menor[1]:
        for img_comparar in maior[1]:
            path_img_atual = os.path.join(menor[0],img_atual)
            path_img_comparar = os.path.join(maior[0],img_comparar)
            
            dhash_atual = le_metadata(path_img_atual)["dhash"]
            dhash_comparar = le_metadata(path_img_comparar)["dhash"]
            distancia_hash = hamming_distance(dhash_atual,dhash_comparar)

            valor = define_intervalo(distancia_hash, "dhash")

            if valor == 1:
                iguais+=1
            elif valor == 2:
                indeterminado+=1

    return classifica_imoveis(iguais,indeterminado,len(menor[1]),menor[0],maior[0])
    

def classifica_imoveis(iguais,indeterminado,tamanho_imovel_atual,path_imovel_atual,path_imovel_a_comparar):
    prop_igual = (iguais)/tamanho_imovel_atual
    prop_ind = (indeterminado)/tamanho_imovel_atual
    diferentes,prop_dif = (tamanho_imovel_atual - iguais - indeterminado,1 - (prop_igual + prop_ind))
    todas_proporcoes = (prop_igual,prop_ind,prop_dif)
    if prop_igual >= PROPORCAO_IGUAIS and diferentes <= DIFERENCA_MAXIMA:
        return (path_imovel_atual, path_imovel_a_comparar, todas_proporcoes, 1)
    elif prop_dif >= PROPORCAO_DIFERENTES:
        return (path_imovel_atual, path_imovel_a_comparar, todas_proporcoes, 3)
    elif (prop_igual <= PROPORCAO_IGUAIS and iguais >=1) or (prop_ind >= PROPORCAO_INDETERMINADOS):
        return (path_imovel_atual, path_imovel_a_comparar, todas_proporcoes, 2)
    else:
        return (path_imovel_atual, path_imovel_a_comparar, todas_proporcoes, -1)
    
def define_intervalo(distancia, tipo):
    if tipo == "dhash":
        if distancia <= DHASH_MIN: # IGUAIS
            return 1
        elif distancia <= DHASH_MAX: # DUVIDOSO
            return 2
        else: # DIFERENTES
            return 3
    elif tipo == "phash":
        print("ainda não implementado")










'''
AQUI EU TENHO QUE CRIAR UM CSV NOVO COM OS IMOVEIS FINAIS QUE NÃO SÃO DUPLICADOS E NEM INDETERMINADOS
TENHO QUE CRIAR UM CSV NOVO COM OS IMOVEIS INDETERMINADOS
    IMOVEL1-IMOVEL2
TENHO QUE CRIAR UM CSV NOVODIZENDO QUE UM IMOVEL É IGUAL AO OUTRO?

'''    

