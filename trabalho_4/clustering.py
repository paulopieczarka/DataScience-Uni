"""
"""
import sys
import os
sys.path.append(os.path.abspath("../helpers"))

import graph
from matplotlib import pyplot as plt
import numpy as np

import pandas as pd
data = pd.read_csv('Cientometria\\resultadoConsultaQualis.txt', names = ["ano","qualisJournalId","areaConhecimentoId","areaConhecimento","qualisScoreValue","grupoName","paperName"])
#"ano","qualisJournalId","areaConhecimentoId","areaConhecimento","qualisScoreValue","grupoName","paperName"
#"2005","0567-7572","12","ENGENHARIAS II","B3","DEAGRO/G","Evaluation of different substrates on african violet (Saintpaulia ionantha Wendl.) growth."


data = data.drop('qualisJournalId',axis=1)
data = data.drop('paperName',axis=1)
#"ano" , "areaConhecimentoId","areaConhecimento" ,"qualisScoreValue", "grupoName"
#"2005", "12"                ,"ENGENHARIAS II"   ,"B3"              , "DEAGRO/G"


data.qualisScoreValue[data.qualisScoreValue == 'A1'] = 1 
data.qualisScoreValue[data.qualisScoreValue == 'A2'] = 0.85 
data.qualisScoreValue[data.qualisScoreValue == 'B1'] = 0.70 
data.qualisScoreValue[data.qualisScoreValue == 'B2'] = 0.55 
data.qualisScoreValue[data.qualisScoreValue == 'B3'] = 0.40 
data.qualisScoreValue[data.qualisScoreValue == 'B4'] = 0.25 
data.qualisScoreValue[data.qualisScoreValue == 'B5'] = 0.10 
data.qualisScoreValue[data.qualisScoreValue == 'C'] = 0.05 

def groupSumSort(data, groupBy, sortBy=False, ascending=True):
    df = data.groupby(by=groupBy).sum()
    df = df[:-1]
    if sortBy:
        df = df.sort_values(by=sortBy, ascending=ascending)
    return df.reset_index()

# imprimindo o score geral por ano
input = data.drop(["grupoName", "areaConhecimentoId","areaConhecimento"], axis=1)
df = groupSumSort(input, ['ano'])
graph.plot_line(
    df['qualisScoreValue'], 
    ylabel='Total Qualis Score', 
    xlabel='Ano'
)

# imprimindo o score geral por grupo
input = data.drop(["ano","areaConhecimentoId","areaConhecimento"], axis=1)
df = groupSumSort(input, ['grupoName'], ['qualisScoreValue'], True)
graph.plot_barh(
    data=df['qualisScoreValue'], 
    names=df['grupoName'], 
    xlabel='Score',
    title='Score geral por grupo'
)

# imprimindo o score geral por area
input = data.drop(["ano","grupoName","areaConhecimentoId"], axis=1)
df = groupSumSort(input, ['areaConhecimento'], ['qualisScoreValue'], False)
graph.plot_barh(
    data=df['qualisScoreValue'], 
    names=df['areaConhecimento'], 
    xlabel='Score',
    title='Score geral por area'
)