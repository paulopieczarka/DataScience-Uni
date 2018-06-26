"""
"""
import sys
import os
sys.path.append(os.path.abspath("../helpers"))

from plotly import plotly as py
from plotly import graph_objs as go

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

def groupSumSort(data, groupBy, sortBy=False, ascending=True, top=False, func='sum'):
    df = data.groupby(by=groupBy)
    
    if func=='sum':
        df = df.sum().reset_index()
    else:
        if func=='mean':
            df = df.mean().reset_index()

    df = df[:-1]
    if sortBy:
        df = df.sort_values(by=sortBy, ascending=ascending)
    if top:
        df = df.groupby(top[0]).head(top[1])
        df = df.sort_values(by=top[0]).reset_index()
    return df

# imprimindo o score geral por ano
input = data.drop(["grupoName", "areaConhecimentoId","areaConhecimento"], axis=1)
df = groupSumSort(input, ['ano'])
# graph.plot_line(
#     df['qualisScoreValue'], 
#     ylabel='Total Qualis Score', 
#     xlabel='Ano',
#     title='Score geral por ano'
# )

# imprimindo o score geral por grupo
input = data.drop(["ano","areaConhecimentoId","areaConhecimento"], axis=1)
df = groupSumSort(input, ['grupoName'], ['qualisScoreValue'], True)
# graph.plot_barh(
#     data=df['qualisScoreValue'], 
#     names=df['grupoName'], 
#     xlabel='Score',
#     title='Score geral por grupo'
# )

# imprimindo o score geral por area
input = data.drop(["ano","grupoName","areaConhecimentoId"], axis=1)
df = groupSumSort(input, ['areaConhecimento'], ['qualisScoreValue'], False)
# graph.plot_barh(
#     data=df['qualisScoreValue'], 
#     names=df['areaConhecimento'], 
#     xlabel='Score',
#     title='Score geral por area'
# )

# imprimingo as 3 areas que mais publicaram
input = data.drop(["grupoName","areaConhecimentoId"], axis=1)
df = groupSumSort(input, ['ano', 'areaConhecimento'], ['ano', 'qualisScoreValue'], [True, False])
gp = df.reset_index().head(3).groupby(['areaConhecimento'])
for area in gp.groups:
    ax.plot('ano', 'qualisScoreValue', data=df[df.areaConhecimento == area], label=area)

# df = input.drop('areaConhecimento', axis=1).groupby('ano').sum()
# print(df)
# ax.plot('ano', 'qualisScoreValue', data=df)

plt.xlabel('Ano de publicação')
plt.ylabel('Total score')
plt.title('3 areas com maior score')
plt.legend()
plt.show()
