import pandas as pd
import os, re
import smoothing_fns as sf

redo = ''

#store variables for locations
symbolsdf = '../data/symbols2008DF.pkl'
symbolsDF = pd.read_pickle(symbolsdf)

datadir = 'data2008'
start, end = '2007-05-02', '2016-04-11'             #variable here
datadir_name = '_'.join((datadir, start, end))
datadir_path = ''.join(('../data/', datadir_name))

# simple smoothing function (regression with slope)
def add_smoothing_fn_cols(df, lookback = 100):                 #variable
    ls, bs = sf.get_smooth_val(df['Adj Close'], lookback)
    df[''.join(('smooth_predict_', str(lookback)))] = ls        #this col to trade_logic.py (smoothcol)
    df[''.join(('smooth_slope_', str(lookback)))] = bs
    return df

def add_kalman_cols(df, tag = ''):
    xs, cov = sf.run(data = df)
    df[''.join(('kalman_predict', tag))] = xs[:,0]     #this col to trade_logic.py (smoothcol)
    df[''.join(('kalman_slope', tag))] = xs[:,1]
    df[''.join(('kalman_a', tag))] = cov[:,0,0]
    df[''.join(('kalman_b', tag))] = cov[:,0,1]
    df[''.join(('kalman_c', tag))] = cov[:,1,0]
    df[''.join(('kalman_d', tag))] = cov[:,1,1]
    return df


symbolDFtag = 'smooth regr'                        #to trade_logic.py (has_smooth_col)
if symbolDFtag not in symbolsDF.columns:
    symbolsDF[symbolDFtag] = False
elif redo==symbolDFtag:
    symbolsDF[symbolDFtag] = False
for symbol in symbolsDF[symbolsDF[symbolDFtag]==False].symbols:
    print(symbol)
    try:
        df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
        df = add_smoothing_fn_cols(df)
        symbolsDF[symbolDFtag][symbol] = True
        df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    except:
        pass
    
symbolDFtag = 'kalman'                              #to trade_logic.py (has_smooth_col)
if symbolDFtag not in symbolsDF.columns:
    symbolsDF[symbolDFtag] = False
elif redo==symbolDFtag:
    symbolsDF[symbolDFtag] = False
for symbol in symbolsDF[symbolsDF[symbolDFtag]==False].symbols:
    print(symbol)
    try:
        df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
        df = add_kalman_cols(df)
        symbolsDF[symbolDFtag][symbol] = True
        df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    except:
        pass
    
symbolsDF.to_pickle(symbolsdf)




#########var map
#in: nothing
#out: line 16/22 to trade_logic (smoothcol)
    # line 31/46 to trade_logic (has_smooth_col)
