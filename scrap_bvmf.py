import pandas as pd
from datetime import datetime

def busca_carteira_teorica(indice):
  url = 'http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice={}&idioma=pt-br'.format(indice.upper())
  return pd.read_html(url, decimal=',', thousands='.', index_col='Código')[0][:-1]

def prepare_data(data):
    df = data.copy()
    date = datetime.now().strftime('%Y-%m-%d')
    df.reset_index(inplace=True)
    df.rename(columns={'Part. (%)':'Part(%)', 'Código': 'index'}, inplace=True)
    df = df[['index','Part(%)']].T
    df.insert(loc=0, column='date', value=['date',date])
    df.columns = df.iloc[0,:]
    df.drop(labels='index' , axis=0, inplace=True)
    df.set_index('date', inplace=True)

    return df
