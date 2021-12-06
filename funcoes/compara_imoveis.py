from logging import disable
import os
import numpy as np
import pandas as pd
import multiprocessing as mp

from funcoes.auxiliares import *

DHASH_MAX = 12
DHASH_MIN = 6

def compara_imoveis(CSV_PATH,FOTOS_PATH,CSV_PATH_OUTPUT):
    percorre_imoveis(CSV_PATH,FOTOS_PATH,CSV_PATH_OUTPUT)

def percorre_imoveis(CSV_PATH,FOTOS_PATH,CSV_PATH_OUTPUT):
    """
        DOCUMENTAR
    """
    df = pd.read_csv(CSV_PATH)
    info = list(zip(df["ecd"],df["cfr"]))
    indeterminados = [] # [[img1,img2],...]
    iguais = []         # [[img1,img2],...]
    diferentes = []     # [img1,...]
    for i in range(len(info)-1):
        print(f"""-------------------------------------------------""")    
        print(f"""-------------------------------------------------""")    
        print(f"""-------------------------------------------------""")  
        imovel_atual = info[i]
        resto = info[i+1:]
        processos = cria_processos(imovel_atual,resto,FOTOS_PATH)
        inicia_processos(processos)
        # break
        
def cria_processos(imovel_atual,lista_imoveis,FOTOS_PATH):
    manager = mp.Manager()
    return_dict = manager.dict()

    n_processos = mp.cpu_count()//4 

    imoveis_split = np.array_split(lista_imoveis,n_processos)
    lista_processos = []
    
    for i in range(n_processos):
        processo = mp.Process(target=percorre_e_compara, args=(imovel_atual,imoveis_split[i],FOTOS_PATH,return_dict))
        lista_processos.append(processo)

    return lista_processos     
        
def inicia_processos(processos):
    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()

def percorre_e_compara(imovel_atual, imoveis,FOTOS_PATH,return_dict):

    path_atual = os.path.join(FOTOS_PATH,os.path.join(str(imovel_atual[0]),str(imovel_atual[1])))
    img_imovel_atual = os.listdir(path_atual)
    for i,imovel_a_comparar in enumerate(imoveis):
        if i%50 == 0: 
            print('PROCESSO ',os.getpid(),' ---> ', i, 'de', len(imoveis), 'feito')

        path_comparar = os.path.join(FOTOS_PATH, os.path.join(str(imovel_a_comparar[0]),str(imovel_a_comparar[1])))
        img_imovel_a_comparar = os.listdir(path_comparar)
        verifica_igualdade(path_atual,img_imovel_atual,path_comparar,img_imovel_a_comparar)


def verifica_igualdade(path_imovel_atual,img_imovel_atual,path_imovel_a_comparar,img_imovel_a_comparar):
    iguais = 0
    indeterminado = 0
    diferentes = 0
    
    '''
        Se eu estou olhando para A e A esta contido em B, 
        então n tem problema, mas se estou olhando para B,
        o valor dos iguais não fara sentido
    '''
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
            else:
                diferentes+=1 

    classifica_imoveis(iguais,indeterminado,len(menor[1]),menor[0],maior[0])
    # print(f"""
    #     ------------------------------------------------
    #     comparando '{menor[0]}' com '{maior[0]}'
    #     <<<iguais = {iguais} diferentes = {diferentes} indeterminados = {indeterminado} tamanho_atual = {len(menor[1])} tamanho_a_comparar = {len(maior[1])}>>> 
    #     igual/imovel_atual  = {(iguais)/len(menor[1])}
    #     indeterminado/imovel_atual  = {(indeterminado)/len(menor[1])}
    #     -------------------------------------------------
    #     """)
    

def classifica_imoveis(iguais,indeterminado,tamanho_imovel_atual,path_imovel_atual,path_imovel_a_comparar):
    prop_igual = (iguais)/tamanho_imovel_atual
    prop_ind = (indeterminado)/tamanho_imovel_atual
    prop_dif = 1 - (prop_igual + prop_ind)
    if prop_dif >= 0.75:
        print(f"""
               relação entre {path_imovel_atual} com {path_imovel_a_comparar}
               DIFERENTES {prop_dif}
               """)
    elif prop_igual >= 0.75:
        print(f"""
               relação entre {path_imovel_atual} com {path_imovel_a_comparar}
               IGUAIS {prop_igual}
               """)
    elif prop_ind >= 0.75:
        print(f"""
               relação entre {path_imovel_atual} com {path_imovel_a_comparar}
               INDETERMINADO {prop_ind}
               """)
    else:
        if prop_ind == 0:
            print(f"""
                relação entre {path_imovel_atual} com {path_imovel_a_comparar}
                IGUAIS {prop_igual}
                DIFERENCIADO {prop_dif}
                prop_igual/prop_dif {prop_igual/prop_dif}
                """)
            
        elif prop_igual == 0:
            print(f"""
                relação entre {path_imovel_atual} com {path_imovel_a_comparar}
                INDETERMINADO {prop_ind}
                DIFERENCIADO {prop_dif}
                prop_ind/prop_dif {prop_ind/prop_dif}
                """)
        elif prop_dif == 0:
            print(f"""
                relação entre {path_imovel_atual} com {path_imovel_a_comparar}
                IGUAIS {prop_igual}
                INDETERMINADO {prop_ind}
                prop_igual/prop_ind {prop_igual/prop_ind}
                """)
   



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

