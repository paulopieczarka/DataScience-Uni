"""
"""
import sys
import os
sys.path.append(os.path.abspath("../helpers"))

import graph
from matplotlib import pyplot as plt
import numpy as np

import pandas as pd
data = pd.read_csv(
    'Cientometria\\resultadoConsultaSJR.txt', 
    header=0,
    names = ["ano","sjrJournalId","areaConhecimento","sjrScoreValue","nomeGrupo","nomeAutor","nomePaper"],
)

data = data.drop('sjrJournalId',axis=1)
data = data.drop('nomePaper',axis=1)

def groupSumSort(data, groupBy, sortBy=False, ascending=True, top=False, func='sum'):
    df = data.groupby(by=groupBy)
    
    if func=='sum':
        df = df.sum()
    else:
        if func=='mean':
            df = df.mean().reset_index()

    df = df[:-1]
    if sortBy:
        df = df.reset_index()
        df = df.sort_values(by=sortBy, ascending=ascending)
    if top:
        df = df.groupby(top[0]).head(top[1])
        df = df.sort_values(by=top[0]).reset_index()
    return df

# imprimindo o score geral por ano
input = data.drop(["nomeGrupo","areaConhecimento"], axis=1)
df = groupSumSort(input, ['ano'])
print(df)
graph.plot_line(
    df['sjrScoreValue'], 
    ylabel='Total Qualis Score', 
    xlabel='Ano',
    title="Score geral por ano"
)

# imprimindo o score geral por grupo
input = data.drop(["ano","areaConhecimento"], axis=1)
df = groupSumSort(input, ['nomeGrupo'], ['sjrScoreValue'], True)
graph.plot_barh(
    data=df['sjrScoreValue'], 
    names=df['nomeGrupo'], 
    xlabel='Score',
    title='Score geral por grupo'
)

# imprimindo o score geral por area
input = data.drop(["ano","nomeGrupo"], axis=1)
df = groupSumSort(input, ['areaConhecimento'], ['sjrScoreValue'], False)
df = df.head(5)
graph.plot_barh(
    data=df['sjrScoreValue'], 
    names=df['areaConhecimento'], 
    xlabel='Score',
    title='Score geral por area'
)

# imprimingo as 3 areas que mais publicaram
input = data.drop(["nomeGrupo"], axis=1)
df = groupSumSort(input, ['ano', 'areaConhecimento'], ['ano', 'sjrScoreValue'], [True, False])

gp = df.reset_index().head(3).groupby(['areaConhecimento'])
for area in gp.groups:
    print(area)
    plt.plot('ano', 'sjrScoreValue', data=df[df.areaConhecimento == area], label=area)

plt.xlabel('Ano de publicação')
plt.ylabel('Total score')
plt.title('3 areas com maior score')
plt.legend()
plt.show()
