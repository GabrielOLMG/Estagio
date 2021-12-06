from logging import disable
import os
import numpy as np
import pandas as pd
import multiprocessing as mp

from funcoes.auxiliares import *

DHASH_MAX = 12
DHASH_MIN = 6

def compara_imoveis(CSV_PATH,FOTOS_PATH):
    percorre_imoveis(CSV_PATH,FOTOS_PATH)

def percorre_imoveis(CSV_PATH,FOTOS_PATH):
    """
        DOCUMENTAR
    """
    df = pd.read_csv(CSV_PATH)
    info = list(zip(df["ecd"],df["cfr"]))

    print(info[0:10])
    # return
    for i in range(len(info)-1):
        print(f"""-------------------------------------------------""")    
        print(f"""-------------------------------------------------""")    
        print(f"""-------------------------------------------------""")  
        imovel_atual = info[i]
        resto = info[i+1:]
        processos = cria_processos(imovel_atual,resto,FOTOS_PATH)
        inicia_processos(processos)
          
        break
        
        
def cria_processos(imovel_atual,lista_imoveis,FOTOS_PATH):
    n_processos = 1#mp.cpu_count()//4 

    imoveis_split = np.array_split(lista_imoveis,n_processos)
    lista_processos = []
    
    for i in range(n_processos):
        processo = mp.Process(target=percorre_e_compara, args=(imovel_atual,imoveis_split[i],FOTOS_PATH))
        lista_processos.append(processo)

    return lista_processos     
        
def inicia_processos(processos):
    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()

def percorre_e_compara(imovel_atual, imoveis,FOTOS_PATH):
    
    path_atual = os.path.join(FOTOS_PATH,os.path.join(str(imovel_atual[0]),str(imovel_atual[1])))
    

    img_imovel_atual = os.listdir(path_atual)
    # print(path_atual,img_imovel_atual)
      
    for i,imovel_a_comparar in enumerate(imoveis):
        if i%50 == 0: 
            print('PROCESSO ',os.getpid(),' ---> ', i, 'de', len(imoveis), 'feito')
        path_comparar = os.path.join(FOTOS_PATH, os.path.join(str(imovel_a_comparar[0]),str(imovel_a_comparar[1])))
        img_imovel_a_comparar = os.listdir(path_comparar)
        verifica_igualdade(path_atual,img_imovel_atual,path_comparar,img_imovel_a_comparar)
        
        break


def verifica_igualdade(path_imovel_atual,img_imovel_atual,path_imovel_a_comparar,img_imovel_a_comparar):
    #path_imovel_atual = os.path.join("\\".join(imovel_atual[1].split('\\')[:-1]),imovel_atual)
    print(f"""-------------------------------------------------
           comparando '{path_imovel_atual}' com '{path_imovel_a_comparar}'
           """)
    iguais = 0
    indeterminado = 0
    diferentes = 0
    for img_atual in img_imovel_atual:
        for img_comparar in img_imovel_a_comparar:
            path_img_atual = os.path.join(path_imovel_atual,img_atual)
            path_img_comparar = os.path.join(path_imovel_a_comparar,img_comparar)

            dhash_atual = calcula_hashs(path_img_atual)[0]
            dhash_comparar = calcula_hashs(path_img_comparar)[0]

            distancia_hash = hamming_distance(dhash_atual,dhash_comparar)

            valor = define_intervalo(distancia_hash, "dhash")

            if valor == 1:
                # tenho que ver qual dos dois tem as melhores imagens, colocar em um csv para depois ver
                iguais+=1
            elif valor == 2:
                indeterminado+=1
            else:
                diferentes+=1 

    print(f"<<<iguais = {iguais} diferentes = {diferentes} indeterminados = {indeterminado} tamanho_atual = {len(img_imovel_atual)} tamanho_a_comparar = {len(img_imovel_a_comparar)}>>>")
    print(f"<<<proporcao igual/indeterminados = {(iguais+1)/(indeterminado+1)}>>>")
    # casos bases
    if(iguais == len(img_imovel_atual)):
        print("REALMENTE SAO IGUAIS")
    elif(indeterminado == len(img_imovel_atual)):
        print("REALMENTE SAO DUVIDOSOS")
    elif (diferentes == (len(img_imovel_atual)*len(img_imovel_a_comparar))):
        print("REALMENTE SAO DIFERENTES")

    print(f"""-------------------------------------------------""")        



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
