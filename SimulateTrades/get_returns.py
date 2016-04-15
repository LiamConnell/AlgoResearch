import pandas as pd
import numpy as np

symbolsDF = pd.read_pickle('../data/symbolsDF.pkl')
start, end = '2007-05-02', '2016-04-11'                        #variable here
datadir_name = '_'.join(('data', start, end))
datadir_path = ''.join(('../data/', datadir_name))

def get_returns(symbol, return_col , pos_col):
    df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    if return_col not in symbolsDF.columns:
        df['daily_rets'] = (df['Adj Close'].shift(-1) - df['Adj Close']) / df['Adj Close']
        #df[return_col]= np.cumprod(df['daily_rets']*df.test +1)
        df[return_col]= df['daily_rets']*df[pos_col]
        df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
    return df

redo=True
got_return_col = 'kal_returns_calc'                            #checkpoint out
if got_return_col not in symbolsDF.columns:
    symbolsDF[got_return_col] = False
elif redo == True:
    symbolsDF[got_return_col] = False
returnsDF = pd.DataFrame()
for symbol in symbolsDF[symbolsDF['kal_logic']==True].symbols: #from trade_logic (added_pos_col)
    print(symbol)
    return_col = 'kal_returns'                                  #out
    df = get_returns(symbol, return_col , pos_col='kal_pos')   #pos from t_l (colname)
    returnsDF[symbol] =df[return_col]
    symbolsDF[got_return_col][symbol] = True
    
    
returnsdir = '../data/kal_returnsDF.pkl'
returnsDF.to_pickle(returnsdir)
print('Returns saved to:')
print(returnsdir)



#########var map
#in: lines 25, 28 for a symbol checkpoint and pos_col
#out: line 27 return_col, line 19 checkpoint