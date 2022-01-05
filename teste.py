import pandas as pd
import os
import json
from collections import Counter
from funcoes.configuracao import *

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
    dados["classe_energetica_id"] = df["classe_energetica_id"].values[0]
    dados["data_public"] = json.loads(df["data_public"].values[0])

    return dados


def camada1(df,dados):
    todos_ids = []
    colunas = ['tipo','classe_energetica_id','garagem','terraco','piscina','terreno']
    for coluna in colunas:
        df_resumido = df.loc[df[coluna] == dados[coluna]]

        todos_ids.extend(list(df_resumido['id']))

    ids_freq = Counter(todos_ids)

    lista_ids = [id_ for id_,frequencia in ids_freq.items() if frequencia >= MIN_IGUAL]
    resto = df[df['id'].isin(lista_ids)]
    return resto


CSV_PATH_METADADO = "CSV_FILES\dados_gabriel.csv"
df = pd.read_csv(CSV_PATH_METADADO)
lista_ids = list(df["id"])
df_copy = df.copy()

for i,id_ in enumerate(lista_ids):
    dados = get_informacoes(df_copy.loc[df_copy["id"] == id_])
    resto = camada1(df_copy,dados)
    if i%100 == 0: print(f"{i} de um total de {len(lista_ids)}")