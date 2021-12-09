#--------------------------------------------------------------------------------#
'''
    input = {"a":["b"], "b":["a","d","c"], "d":["b","q"], "c":["b"], "q":["d"], "r":["r2"], "r2":["r"]}
    output parecido com = {'q': ['d', 'b', 'a', 'c'], 'r': ['r2'], 'r2': ['r']}
    
    explicando:
        se a = b e b = c, então a = [b,c]
'''
def getList(elemento, duplicadas,vistos):
    if elemento in vistos:
        '''caso base'''
        return [] 
    lista_atual = duplicadas[elemento]
    atual = [elemento]
    vistos.append(elemento)
    
    for elementoN in lista_atual:
        atual.extend(getList(elementoN,duplicadas,vistos))

    return atual
    
def simplificaDuplicadas(duplicadas):
    vistos = []
    duplicadas_c = duplicadas.copy()
    para_analisar = []
    for key in duplicadas_c:
        if(key in vistos): continue
        teste = getList(key,duplicadas, vistos)
        para_analisar.append(teste)
    return para_analisar

#--------------------------------------------------------------------------------#
from imagededup.methods import PHash, DHash

def calcula_hashs(PATH_IMAGEM):
    """
        DOCUMENTAR
    """
    phash, dhash= PHash(),DHash()

    encodings_phash = phash.encode_image(image_file=PATH_IMAGEM)
    encodings_dhash = dhash.encode_image(image_file=PATH_IMAGEM)
    
    return encodings_dhash,encodings_phash        

#--------------------------------------------------------------------------------#
import numpy as np
def hamming_distance(hash1, hash2):
        """
        Calculate the hamming distance between two hashes. If length of hashes is not 64 bits, then pads the length
        to be 64 for each hash and then calculates the hamming distance.
        Args:
            hash1: hash string
            hash2: hash string
        Returns:
            hamming_distance: Hamming distance between the two hashes.
        """
        hash1_bin = bin(int(hash1, 16))[2:].zfill(
            64
        )  # zfill ensures that len of hash is 64 and pads MSB if it is < A
        hash2_bin = bin(int(hash2, 16))[2:].zfill(64)
        return np.sum([i != j for i, j in zip(hash1_bin, hash2_bin)])

#--------------------------------------------------------------------------------#
import json
import piexif
import piexif.helper
def le_metadata(PATH_IMAGEM):
    """
        DOCUMENTAR
    """

    exif_dict = piexif.load(PATH_IMAGEM)
    user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
    hash = json.loads(user_comment)
    return hash

#--------------------------------------------------------------------------------#
import pandas as pd
import os

def cria_csv(CSV_PATH,valores):
    dicionario = {"imovel1":valores["imovel1"],
                  "imovel2" :valores["imovel2"],
                  "proporcao_de_iguais" : valores["proporcao_de_iguais"],
                  "proporcao_de_diferentes" : valores["proporcao_de_diferentes"],
                  "proporcao_de_indeterminados" : valores["proporcao_de_indeterminados"]}
    df = pd.DataFrame(dicionario)
    df.to_csv(CSV_PATH,index=False)

def atualiza_csv(CSV_PATH, lista):
    print("COLOCA NO CSV", lista)
    iguais = {"imovel1":[], "imovel2" :[],"proporcao_de_iguais" :[],"proporcao_de_diferentes" :[],"proporcao_de_indeterminados" :[]}
    diferentes = {"imovel1":[], "imovel2" :[],"proporcao_de_iguais" :[],"proporcao_de_diferentes" :[],"proporcao_de_indeterminados" :[]}
    indeterminados = {"imovel1":[], "imovel2" :[],"proporcao_de_iguais" :[],"proporcao_de_diferentes" :[],"proporcao_de_indeterminados" :[]}

    for imovel1,imovel2,proporcao,resultado in lista:
        escolhido = None
        print(os.getpid(),imovel1)
        if resultado == 1:
            escolhido = iguais
            csv_file = os.path.join(CSV_PATH,"iguais.csv")
        elif resultado == 3:
            escolhido = diferentes
            csv_file = os.path.join(CSV_PATH,"diferentes.csv")
        else:
            escolhido = indeterminados
            csv_file = os.path.join(CSV_PATH,"indeterminados.csv")
        
        escolhido["imovel1"].append(imovel1.split('\\')[-1])
        escolhido["imovel2"].append(imovel2.split('\\')[-1])
        escolhido["proporcao_de_iguais"].append(proporcao[0])
        escolhido["proporcao_de_diferentes"].append(proporcao[2])
        escolhido["proporcao_de_indeterminados"].append(proporcao[1])
        escolhido = pd.DataFrame(escolhido)

    iguais = pd.DataFrame(iguais)
    diferentes = pd.DataFrame(diferentes)
    indeterminados = pd.DataFrame(indeterminados)
    try: # Ve se csv ja existe
        df = pd.read_csv(csv_file)
        iguais.to_csv(os.path.join(CSV_PATH,"iguais.csv"), mode='a', header=False,index=False)
        diferentes.to_csv(os.path.join(CSV_PATH,"diferentes.csv"), mode='a',header=False,index=False)
        indeterminados.to_csv(os.path.join(CSV_PATH,"indeterminados.csv"), mode='a',header=False,index=False)
    except: # Se não existe, cria um novo
        cria_csv(csv_file,escolhido)
        df = pd.read_csv(csv_file)
        iguais.to_csv(os.path.join(CSV_PATH,"iguais.csv"), mode='a',index=False)
        diferentes.to_csv(os.path.join(CSV_PATH,"diferentes.csv"), mode='a',index=False)
        indeterminados.to_csv(os.path.join(CSV_PATH,"indeterminados.csv"), mode='a',index=False)
    

    iguais.to_csv(os.path.join(CSV_PATH,"iguais.csv"), mode='a', header=False,index=False)
    diferentes.to_csv(os.path.join(CSV_PATH,"diferentes.csv"), mode='a',index=False)
    indeterminados.to_csv(os.path.join(CSV_PATH,"indeterminados.csv"), mode='a',index=False)


#--------------------------------------------------------------------------------#

def gera_inputs_pool(imovel_atual,imoveis_split, FOTOS_PATH):
    input_ = []
    for i in range(len(imoveis_split)):
        input_.append((imovel_atual,imoveis_split[i],FOTOS_PATH))
    return input_