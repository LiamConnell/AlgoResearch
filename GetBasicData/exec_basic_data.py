import pandas as pd
import get_symbols
import os, re
import pandas.io.data as web

#make sure file system has data directory
if os.path.exists('../data/') == False:
    os.makedirs('../data/')

symbolsdf = '../data/symbols2008DF.pkl'
#create or load symbolsDF
if os.path.exists(symbolsdf) == False:
    sp = pd.read_csv('/Users/liamconnell/Downloads/HistoricalSP500.csv')
    symbolsDF = pd.DataFrame(sp[sp['2008'] == 'X'].Ticker.tolist())
    symbolsDF.columns = ['symbols']
    symbolsDF.index = symbolsDF.symbols
    symbolsDF.to_pickle(symbolsdf)
else:
    symbolsDF = pd.read_pickle(symbolsdf)

#load raw financial data in new folder              #as function
datadir = 'data2008'
start, end = '2007-05-02', '2016-04-11'             #variable here
datadir_name = '_'.join((datadir, start, end))
datadir_path = ''.join(('../data/', datadir_name))

if os.path.exists(datadir_path) == False:
    os.makedirs(datadir_path)
    symbolsDF[datadir_name] = False
    symbolsDF['startdate'] = None
    symbolsDF['enddate'] = None
    for symbol in symbolsDF.symbols:
        try:
            print(symbol)
            df = web.DataReader(symbol, 'yahoo', start, end)
            df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
            symbolsDF[datadir_name][symbol] = True
            symbolsDF['startdate'][symbol] = df.index[0]
            symbolsDF['enddate'][symbol] = df.index[-1]
        except:
            print('DIDNT WORK!!!!!!!!!')
        
symbolsDF.to_pickle(symbolsdf)
