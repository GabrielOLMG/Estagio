import json
import numpy as np
import pandas as pd


from configuracao import INTERVALO_AREA, CAMADA1, CAMADA2, CAMADA3

"""
    Ideia: separar em  camadas de comparação, se passar da primeira 
    então verifico a segunda e assim vai seguindo, caso contrario então dois imoveis
    são definidos como diferentes.

    - tipo (Se é um partamento ou Morada) ()
    - tipologia (t1,t2)()
    - garagem,terraco,piscina,terreno()
    - 'data_public'-abp, verificar se são iguais com uma determinada margem de erro ()
    - freguesia_id
    - regiao_id
    - classe_energetica_id ()

    

"""

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
    resto = df.loc[df["regiao_id"] == dados["regiao"]]
    resto = resto.loc[df["freguesia_id"] == dados["freguesia"]]
    resto = resto.loc[df["tipologia"] == dados["tipologia"]]
    return resto

    

if __name__ == "__main__":
    df = pd.read_csv("..\\CSV_FILES\dados_gabriel.csv")
    df_copy = df.copy()
    for i,id_ in enumerate(list(df["id"])):
        print(f"\nANALISANDO ID {id_}")
        dados = get_informacoes(df.loc[df["id"] == id_])
        print(f"Original {len(df)}")
        if CAMADA1:
            df_copy = camada1(df,dados)
            # print(f"Depois camada1 {len(df_copy)}")
            if len(df_copy) == 1: continue
        if CAMADA2:
            df_copy = camada2(df_copy,dados)
            # print(f"Depois camada2 {len(df_copy)}")
            if len(df_copy) == 1: continue
        if CAMADA3:
            df_copy = camada3(df_copy,dados)
            # print(f"Depois camada3 {len(df_copy)}")
            # if len(df_copy == 1): continue

        if len(df_copy) >1:
            print(df_copy[["cfr","ecd"]])
            print()
        
        
        if i == 2: break
        
        df_copy = df.copy()