import pandas as pd
import os, re
import smoothing_fns as sf

symbolsDF = pd.read_pickle('../data/symbolsDF.pkl')
start, end = '2007-05-02', '2016-04-11'                        #variable here
datadir_name = '_'.join(('data', start, end))
datadir_path = ''.join(('../data/', datadir_name))

def add_smoothing_fn_cols(df, lookback = 100):                 #variable
    ls, bs = sf.get_smooth_val(df['Adj Close'], lookback)
    df[''.join(('smooth_predict_', str(lookback)))] = ls
    df[''.join(('smooth_slope_', str(lookback)))] = bs
    return df

def add_kalman_cols(df, tag = ''):
    xs, cov = sf.run(data = df)
    df[''.join(('kalman_predict', tag))] = xs[:,0]
    df[''.join(('kalman_slope', tag))] = xs[:,1]
    df[''.join(('kalman_a', tag))] = cov[:,0,0]
    df[''.join(('kalman_b', tag))] = cov[:,0,1]
    df[''.join(('kalman_c', tag))] = cov[:,1,0]
    df[''.join(('kalman_d', tag))] = cov[:,1,1]
    return df

if 'smoothing_fns' not in symbolsDF.columns:
    symbolsDF["smoothing_fns"] = False
for symbol in symbolsDF[symbolsDF["smoothing_fns"]==False].symbols:
    try:
        df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
        df = add_smoothing_fn_cols(df)
        symbolsDF["smoothing_fns"][symbol] = True
        df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    except:
        pass
    
if 'kalman' not in symbolsDF.columns:
    symbolsDF["kalman"] = False
for symbol in symbolsDF[symbolsDF["kalman"]==False].head().symbols:
    try:
        df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
        df = add_kalman_cols(df)
        symbolsDF["kalman"][symbol] = True
        df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    except:
        pass
    
symbolsDF.to_pickle('../data/symbolsDF.pkl')