import pandas as pd
import os, re

redo = ''

symbolsDF = pd.read_pickle('../data/symbolsDF.pkl')
start, end = '2007-05-02', '2016-04-11'                        #variable here
datadir_name = '_'.join(('data', start, end))
datadir_path = ''.join(('../data/', datadir_name))


def get_historical_positions(df, smoothcol, pos_colname):
    df['resids'] = df['Adj Close']-df[smoothcol]
    df[pos_colname] = ((df['resids']>0)-.5)*2
    df[pos_colname][df['resids'].isnull()] = 0
    df[pos_colname][((df['resids']==pd.rolling_max(df['resids'], 10)).astype(int) + 
          (df['resids']>0).astype(int))==2]=0
    df[pos_colname][((df['resids']==pd.rolling_min(df['resids'], 10)).astype(int) + 
          (df['resids']<0).astype(int))==2]=0
    return df

def execute_for_symbols(smoothcol, pos_colname, added_pos_col, has_smooth_col, redo=False):
    if added_pos_col not in symbolsDF.columns:
        symbolsDF[added_pos_col] = False
    elif redo == True:
        symbolsDF[added_pos_col] = False
    for symbol in symbolsDF[symbolsDF[added_pos_col]==False].symbols:
        print(symbol)
        if symbolsDF[has_smooth_col][symbol]==True:
            #print(symbol)
            df = pd.read_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
            df = get_historical_positions(df, smoothcol, pos_colname)
            df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
            symbolsDF[added_pos_col][symbol] = True
    symbolsDF.to_pickle('../data/symbolsDF.pkl')
    return
    
if __name__ == "__main__":
    execute_for_symbols(smoothcol='kalman_predict', pos_colname='test_kal', added_pos_col= 'kal_logic', has_smooth_col='kalman', redo=True)
    
    
#########var map
#in: smoothcol, has_smooth_col (39) from add_data
#out: pos_colname, added_pos_col (39) to get_return