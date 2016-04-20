import pandas as pd
import get_symbols
import os, re
import pandas.io.data as web

#make sure file system has data directory
if os.path.exists('../data/') == False:
    os.makedirs('../data/')

#create or load symbolsDF
if os.path.exists('../data/symbolsDF.pkl') == False:
    symbolsDF = pd.DataFrame(get_symbols.main())
    symbolsDF.columns = ['symbols']
    symbolsDF.index = symbolsDF.symbols
    symbolsDF.to_pickle('../data/symbolsDF.pkl')
else:
    symbolsDF = pd.read_pickle('../data/symbolsDF.pkl')

#load raw financial data in new folder              #as function
start, end = '2007-05-02', '2016-04-11'             #variable here
datadir_name = '_'.join(('data', start, end))
datadir_path = ''.join(('../data/', datadir_name))

if os.path.exists(datadir_path) == False:
    os.makedirs(datadir_path)
    symbolsDF[datadir_name] = False
    symbolsDF['startdate'] = None
    symbolsDF['enddate'] = None
    for symbol in symbolsDF.symbols:
        try:
            df = web.DataReader(symbol, 'yahoo', start, end)
            df.to_pickle(''.join((datadir_path, '/', symbol, '.pkl')))
            symbolsDF[datadir_name][symbol] = True
            symbolsDF['startdate'][symbol] = df.index[0]
            symbolsDF['enddate'][symbol] = df.index[-1]
        except:
            pass
        
symbolsDF.to_pickle('../data/symbolsDF.pkl')
