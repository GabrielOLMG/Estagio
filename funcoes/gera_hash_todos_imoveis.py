import os
import json
import piexif
import numpy as np
import pandas as pd
import piexif.helper
import multiprocessing as mp

from PIL import Image
from funcoes.auxiliares import *
from imagededup.methods import PHash, DHash
from funcoes.configuracao import *

def gera_hash_todos_imoveis(CSV_PATH,PATH_FOTOS):
    """
        Gera Hash para todos os imoveis e apaga as imagens repetidas dentro de cada imovel
        DOCUMENTAR
    """

    percorre_pastas(CSV_PATH,PATH_FOTOS)

def percorre_pastas(CSV_PATH,PATH_FOTOS):
    """
        DOCUMENTAR
    """
    df = pd.read_csv(CSV_PATH)
    info = list(zip(df["ecd"],df["cfr"]))
    processos = cria_processos(info,PATH_FOTOS)
    inicia_processos(processos)

def cria_processos(LIST_PATH_IMOVEIS,PATH_FOTOS):
    imoveis_split = np.array_split(LIST_PATH_IMOVEIS,N_PROCESSOS)
    lista_p = []
    for i in range(N_PROCESSOS):
        processo = mp.Process(target=percorre_imoveis, args=(imoveis_split[i],PATH_FOTOS))
        lista_p.append(processo)
    
    return lista_p

def inicia_processos(processos):
    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()        

def percorre_imoveis(IMOVEIS,PATH_FOTOS):
    """
        DOCUMENTAR
    """
    
    
    for i,imovel in enumerate(IMOVEIS):
        path_imovel = os.path.join(PATH_FOTOS,os.path.join(str(imovel[0]),str(imovel[1])))
        percorre_imovel(path_imovel)

        if i%50 == 0: 
            print(os.getpid(),' ---> ', i, '-', len(IMOVEIS))

def percorre_imovel(PATH_IMOVEL):
    """
        DOCUMENTAR
    """

    imagens = os.listdir(PATH_IMOVEL)
    imagensL = []
    phash = []
    dhash = []

    for imagem in imagens:
        path_imagem = os.path.join(PATH_IMOVEL,imagem)
        dh,ph,_,new_name = le_metadata(path_imagem)
        imagensL.append(new_name)
        phash.append(ph)
        dhash.append(dh)


    encontra_iguais(dhash,phash,imagensL,PATH_IMOVEL)


def encontra_iguais(dhash,phash, imagens,PATH_IMOVEL):
    dhash_dic = dict(zip(imagens,dhash))
    # phash_dic = dict(zip(imagens,phash))

    dhash_c = DHash()
    # phash_c = PHash()
    
    dhash_dup = dhash_c.find_duplicates(encoding_map = dhash_dic,max_distance_threshold = 6)
    duplicadas = simplificaDuplicadas(dhash_dup)
    para_remover = analisa_duplicadas(duplicadas,PATH_IMOVEL)
    if DELETE: 
        
        remove_imagem_duplicada(para_remover)
        print(f"""
            #-------------------------------#
            removidos {len(para_remover)} na pasta {PATH_IMOVEL}
            #-------------------------------#
            """)
    else:
        print(f"""
            #-------------------------------#
            ATIVE A VARIAVEL DELETE PARA REALMENTE APAGAR AS IMAGENS REPETIDAS.
            AS SEGUINTES IMAGENS DEVERIAM SER DELETADAS:
            {para_remover} na pasta {PATH_IMOVEL}
            #-------------------------------#
            """)
        
    

def analisa_duplicadas(duplicadas,PATH_IMOVEL):    
    '''
    duplicadas esta recebendo algo como : [['a', 'b', 'c'], ['r', 'p'], ['v']]
    '''
    para_remover = []
    for duplicadas_iguais in duplicadas:
        maior_tamanho = 0
        maior_nome = None
        for image_name in  duplicadas_iguais:
            # path_image = os.path.join(PATH_IMOVEL, image_name)
            image = Image.open(image_name)
            width, height = image.size
            area = width*height
            if area > maior_tamanho:
                if maior_nome is not None: para_remover.append(maior_nome)
                maior_nome = image_name
                maior_tamanho = area
            else:
                para_remover.append(image_name)
                

    return para_remover

def remove_imagem_duplicada(para_remover):
    '''
    para_remover esta recebendo algo como : ['path/img1.jpg','path/img2.jpg']
    '''
    for imagem in para_remover:
        if not os.path.isfile(imagem): continue
        os.remove(imagem)




