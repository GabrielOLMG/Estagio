import os
import json
import numpy as np
import pandas as pd

from multiprocessing import Pool
from funcoes.auxiliares import simplificaDuplicadas, gera_inputs_pool_csv
from funcoes.configuracao import INTERVALO_AREA, CAMADA1, CAMADA2, CAMADA3, N_PROCESSOS_CSV

def acha_duplicadas_csv(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    
    iguais_dic = cria_processos(list(df["id"]),df)
    print(iguais_dic)

def cria_processos(lista_ids,df):
    dic_total = {}
    ids_split = np.array_split(lista_ids,N_PROCESSOS_CSV)
    inputs_ = gera_inputs_pool_csv(ids_split,df)
    with Pool(processes=N_PROCESSOS_CSV) as pool:
        valores = pool.starmap(procura_igual,inputs_)
    for i in valores:
        dic_total.update(i)
    
    return simplificaDuplicadas(dic_total)



def procura_igual(ids,df):
    iguais_dic = {}
    df_copy = df.copy()
    for i,id_ in enumerate(ids):
        dados = get_informacoes(df_copy.loc[df_copy["id"] == id_])
        if CAMADA1:
            df_copy = camada1(df_copy,dados)
            # if len(df_copy) == 1: continue
        if CAMADA2:
            df_copy = camada2(df_copy,dados)
            # if len(df_copy) == 1: continue
        if CAMADA3:
            df_copy = camada3(df_copy,dados)
            # if len(df_copy) == 1: continue
        
        if len(df_copy) >1:
            codigo = str(df.loc[df["id"] == id_]["cfr"].values[0]) + '-' + str(df.loc[df["id"] == id_]["ecd"].values[0])
            iguais_list = [f"{p}-{q}" for p,q in zip(list(df_copy["cfr"]),list(df_copy["ecd"]))]
            iguais_list.remove(codigo)
            iguais_dic[codigo] = iguais_list
            
        df_copy = df.copy()
        if i%1000 == 0:
            print('PROCESSO ',os.getpid(),' ---> ', i, 'de', len(ids), 'feito')
    
    return iguais_dic

def get_informacoes(df):
    dados = {}
    dados["tipo"] = df["tipo"].values[0]
    dados["tipologia"] = df["tipologia"].values[0]
    dados["garagem"] = df["garagem"].values[0]
    dados["terraco"] = df["terraco"].values[0]
    dados["piscina"] = df["piscina"].values[0]
    dados["terreno"] = df["terreno"].values[0]
    dados["freguesia"] = df["freguesia_id"].values[0]
    dados["regiao"] = df["regiao_id"].values[0]
    dados["classe_energetica"] = df["classe_energetica_id"].values[0]
    dados["data_public"] = json.loads(df["data_public"].values[0])

    return dados

def camada1(df,dados):
    resto = df.loc[(df["tipo"] == dados["tipo"]) &
               (df["classe_energetica_id"] == dados["classe_energetica"]) &
               (df["garagem"] == dados["garagem"]) &
               (df["terraco"] == dados["terraco"]) &
               (df["piscina"] == dados["piscina"]) &
               (df["terreno"] == dados["terreno"])]            
    return resto

def camada2(df,dados):
    df2 = df.data_public.apply(json.loads)
    df2_ = pd.DataFrame(list(df2), index=df2.index)

    filtrados = df2_.loc[((dados["data_public"]["abp"]*(1-INTERVALO_AREA)) <= df2_["abp"]) & 
                     ((dados["data_public"]["abp"]*(1+INTERVALO_AREA)) >= df2_["abp"])]   
    resto = df.loc[list(filtrados.index)]
    return resto                 

def camada3(df, dados):
    resto = df.copy()
    resto = resto.loc[resto["regiao_id"] == dados["regiao"]]
    resto = resto.loc[resto["freguesia_id"] == dados["freguesia"]]
    resto = resto.loc[resto["tipologia"] == dados["tipologia"]]
    return resto

    

if __name__ == "__main__":
    pass