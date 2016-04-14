import pandas as pd
import os, re

symbolsDF = pd.read_pickle('../data/symbolsDF.pkl')
start, end = '2007-05-02', '2016-04-11'                        #variable here
datadir_name = '_'.join(('data', start, end))
datadir_path = ''.join(('../data/', datadir_name))


def get_historical_positions(df, smoothcol, colname='test'):
    df['resids'] = df['Adj Close']-df[smoothcol]
    df[colname] = ((df['resids']>0)-.5)*2
    df[colname][df['resids'].isnull()] = 0
    df[colname][((df['resids']==pd.rolling_max(df['resids'], 10)).astype(int) + 
          (df['resids']>0).astype(int))==2]=0
    df[colname][((df['resids']==pd.rolling_min(df['resids'], 10)).astype(int) + 
          (df['resids']<0).astype(int))==2]=0
    return df

def exec_for_symbol(symbol, smoothcol, colname='test'):
    df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    df = get_historical_positions(df, smoothcol, colname)
    df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    return

if 'smoothing_fns_logic' not in symbolsDF.columns:
    symbolsDF["smoothing_fns_logic"] = False
for symbol in symbolsDF[symbolsDF["smoothing_fns_logic"]==False].symbols:
    if symbolsDF['smoothing_fns'][symbol]==True:
        exec_for_symbol(symbol, smoothcol='smooth_predict_100' )
        symbolsDF["smoothing_fns_logic"][symbol] = True
symbolsDF.to_pickle('../data/symbolsDF.pkl')