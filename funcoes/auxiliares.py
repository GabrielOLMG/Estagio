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
    try:    
        lista_atual = duplicadas[elemento]
    except:
        lista_atual = []
    atual = [elemento]
    vistos.append(elemento)
    
    for elementoN in lista_atual:
        l = getList(elementoN,duplicadas,vistos)
        
        atual.extend(l)

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
from PIL import Image



def le_metadata(PATH_IMAGEM):
    """
        DOCUMENTAR
    """
    dh,ph = None,None
    try:
        exif_dict = piexif.load(PATH_IMAGEM)
        user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
        hash = json.loads(user_comment)
        dh = hash["dhash"]
        ph = hash["phash"]
    except: # caso de algum erro no loads ou user_comment ou pegar as devidas keys, ele devera 
        dh,ph = calcula_hashs(PATH_IMAGEM)
        print("rec " + PATH_IMAGEM)
        PATH_IMAGEM = add_metadata(PATH_IMAGEM,{"dhash":dh, "phash":ph})
        return le_metadata(PATH_IMAGEM)
    return dh,ph,hash,PATH_IMAGEM

def add_metadata(PATH_IMAGEM, HASH_IMAGEM):
    """
        IRA ESCREVER NO METADATA DA IMAGEM OS SEUS DEVIDOS HASHS

        :param PATH_IMAGEM = path da imagem
        :param HASH_IMAGEM = dicionario contendo os hash
    """
    try:
        exif_dict = piexif.load(PATH_IMAGEM)
        
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(json.dumps(HASH_IMAGEM), encoding="unicode")
        piexif.insert(piexif.dump(exif_dict),PATH_IMAGEM)
    except:
        # piexif não suporta PNG, então vou passar de PNG para JPG
        imagem = Image.open(PATH_IMAGEM)
        imagemRGB = imagem.convert('RGB')
        novo_nome = PATH_IMAGEM.split('.')[0] + '.jpg'
        os.remove(PATH_IMAGEM) # remove a imagem antiga
        imagemRGB.save(novo_nome)
        
        try: 
            exif_dict = piexif.load(novo_nome)
            exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(json.dumps(HASH_IMAGEM), encoding="unicode")
            piexif.insert(piexif.dump(exif_dict),novo_nome)
            return novo_nome
        except:
            print(f"ERRO Novo Nome = {novo_nome} Antigo Nome = {PATH_IMAGEM}")
            #volta a como estava antes
            os.remove(novo_nome)
            imagem.save(PATH_IMAGEM)
    return PATH_IMAGEM
#--------------------------------------------------------------------------------#
import pandas as pd
import os

def cria_csv(CSV_PATH):
    try:
        pd.read_csv(CSV_PATH)
    except:
        dicionario = {"imovel1":[],
                      "imovel2" :[],
                      "proporcao_de_iguais" : [],
                      "proporcao_de_diferentes" : [],
                      "proporcao_de_indeterminados" : []}
        df = pd.DataFrame(dicionario)
        df.to_csv(CSV_PATH,index=False)

def atualiza_csv(CSV_PATH, lista):
     # esta colocando a mesma informação no csv
     # n esta vendo se tem no ideterminado ou igual antes de colocar no diferente
    iguais = {"imovel1":[], "imovel2" :[],"proporcao_de_iguais" :[],"proporcao_de_diferentes" :[],"proporcao_de_indeterminados" :[]}
    diferentes = {"imovel1":[], "imovel2" :[],"proporcao_de_iguais" :[],"proporcao_de_diferentes" :[],"proporcao_de_indeterminados" :[]}
    indeterminados = {"imovel1":[], "imovel2" :[],"proporcao_de_iguais" :[],"proporcao_de_diferentes" :[],"proporcao_de_indeterminados" :[]}

    for imovel1,imovel2,proporcao,resultado in lista:
        escolhido = None
        if resultado == 1:
            escolhido = iguais
        elif resultado == 3:
            escolhido = diferentes
        else:
            escolhido = indeterminados
        
        escolhido["imovel1"].append(imovel1.split('\\')[-1])
        escolhido["imovel2"].append(imovel2.split('\\')[-1])
        escolhido["proporcao_de_iguais"].append(proporcao[0])
        escolhido["proporcao_de_diferentes"].append(proporcao[2])
        escolhido["proporcao_de_indeterminados"].append(proporcao[1])

    # diferentes = pd.DataFrame(diferentes)
    # csv_diferentes = os.path.join(CSV_PATH,"diferentes.csv")
    # cria_csv(csv_diferentes)
    # diferentes.to_csv(csv_diferentes, mode='a', index=False, header=False)
    
    iguais = pd.DataFrame(iguais)
    csv_iguais = os.path.join(CSV_PATH,"iguais.csv")
    cria_csv(csv_iguais)
    iguais.to_csv(csv_iguais, mode='a', index=False, header=False)

    indeterminados = pd.DataFrame(indeterminados)
    csv_indeterminados = os.path.join(CSV_PATH,"indeterminados.csv")
    cria_csv(csv_indeterminados)
    indeterminados.to_csv(csv_indeterminados, mode='a', index=False, header=False)



#--------------------------------------------------------------------------------#



def gera_inputs_pool_imovel(imoveis_split, FOTOS_PATH):
    input_ = []
    for i in range(len(imoveis_split)):
        input_.append((imoveis_split[i],FOTOS_PATH))
    return input_


def gera_inputs_pool_csv(ids_split,df):
    input_ = []
    for i in range(len(ids_split)):
        input_.append((ids_split[i],df))
    return input_