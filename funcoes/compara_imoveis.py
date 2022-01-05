import ast
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
    info = list(zip(df["Nome"],df["lista_iguais"]))
    cria_processos(info,FOTOS_PATH,CSV_PATH_OUTPUT)

def cria_processos(info,FOTOS_PATH,CSV_PATH_OUTPUT):
    imoveis_split = np.array_split(info,N_PROCESSOS)    
    inputs_list = gera_inputs_pool_imovel(imoveis_split,FOTOS_PATH)
    
    with Pool(processes=N_PROCESSOS) as pool:
        valores = pool.starmap(percorre_candidados_iguais,inputs_list)
    flat_list = [item for sublist in valores for item in sublist]
    atualiza_csv(CSV_PATH_OUTPUT,flat_list) 

def percorre_candidados_iguais(lista_para_comparar,FOTOS_PATH):
    resultados = []
    for i,comparavel in enumerate(lista_para_comparar):
        para_comparar = ast.literal_eval(comparavel[1]) + [comparavel[0]]
        resultado = compara_possiveis_iguais(para_comparar,FOTOS_PATH)
        resultados.extend(resultado)
        if i%50 == 0: 
            print(os.getpid(),' ---> ', i, '-', len(lista_para_comparar))
    return resultados


def compara_possiveis_iguais(lista_para_comparar,FOTOS_PATH):
    resultados = []
    for i,imovel1 in enumerate(lista_para_comparar):
        nome_imovel1,nome_pasta1 = imovel1.split("-")
        path_imovel1 = os.path.join(FOTOS_PATH,os.path.join(nome_pasta1,nome_imovel1))
        img_imovel1 = os.listdir(path_imovel1)

        for imovel2 in list(lista_para_comparar)[i+1:]:
            nome_imovel2,nome_pasta2 = imovel2.split("-")
            path_imovel2 = os.path.join(FOTOS_PATH,os.path.join(nome_pasta2,nome_imovel2))
            img_imovel2 = os.listdir(path_imovel2)
            resultado = verifica_igualdade(path_imovel1,img_imovel1,path_imovel2,img_imovel2)
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
            try:
                _,_,info_atual,_ = le_metadata(path_img_atual)
                dhash_atual = info_atual["dhash"]
            except:
                print("Erro ao ler dhash_atual ",path_img_atual)
                continue
            try:
                _,_,info_comparar,_ = le_metadata(path_img_comparar)
                dhash_comparar = info_comparar["dhash"]
            except:
                print("Erro ao ler a dhash_comparar ",path_img_comparar)
                continue

            distancia_hash = hamming_distance(dhash_atual,dhash_comparar)

            valor = define_intervalo(distancia_hash, "dhash")

            if valor == 1:
                iguais+=1
                break
            elif valor == 2:
                indeterminado+=1
                break

    return classifica_imoveis(iguais,indeterminado,len(menor[1]),menor[0],maior[0])
    

def classifica_imoveis(iguais,indeterminado,tamanho_imovel_atual,path_imovel_atual,path_imovel_a_comparar):
    
    prop_igual = (iguais)/tamanho_imovel_atual # se no imovel1 tem uma imagem e no imovel 2 ele acha 2 iguais ao 1, entao fica 2/1, q e maior q 1
    prop_ind = (indeterminado)/tamanho_imovel_atual
    diferentes,prop_dif = (tamanho_imovel_atual - iguais - indeterminado,1 - (prop_igual + prop_ind))
    todas_proporcoes = (prop_igual,prop_ind,prop_dif)
    # print(f"iguais = {iguais} indeterminado = {indeterminado} diferentes = {diferentes} tamanho_imovel_atual = {tamanho_imovel_atual}")
    
    if prop_igual >= PROPORCAO_IGUAIS and diferentes <= DIFERENCA_MAXIMA and iguais >= IGUAIS_MINIMA:
        return (path_imovel_atual, path_imovel_a_comparar, todas_proporcoes, 1)
    elif prop_dif >= PROPORCAO_DIFERENTES:
        return (path_imovel_atual, path_imovel_a_comparar, todas_proporcoes, 3)
    elif (prop_igual <= PROPORCAO_IGUAIS and iguais >=1) or (prop_ind >= PROPORCAO_INDETERMINADOS) or (iguais < IGUAIS_MINIMA):
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

