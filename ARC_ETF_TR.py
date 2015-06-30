'''
ARC ETF Total Return Calculation
'''

import pandas as pd
import numpy as np

etf_price_data = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying ETF Price Data.csv',index_col=['Date','Ticker'],parse_dates='Date',dayfirst=True)
etf_price_data = etf_price_data.unstack()

etf_price_data = etf_price_data.resample('D',fill_method='ffill')
etf_price_data.fillna(value=0,inplace=True)


etf_div_data = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying ETF Dividend Data.csv',parse_dates='Ex_Div',dayfirst=True,index_col=['Ex_Div','Ticker'])
etf_div_data.sort_index(inplace=True)
etf_div_data = etf_div_data.groupby(level=[0,1]).sum()
etf_div_data = etf_div_data.unstack()
etf_div_data = etf_div_data.resample('D')

#etf_div_data.fillna(value=0,inplace=True)

date_range = pd.date_range(etf_price_data.index.min(),etf_div_data.index.max())

etf_div_data = etf_div_data.ix[date_range]
etf_price_data = etf_price_data.ix[date_range]

#Provides denominator for today/yesterday
A = etf_price_data.subtract(etf_div_data,fill_value=0)
#not working!
B = etf_price_data/A.shift(1)
B.drop(B.tail(1).index,inplace=True)
B = B.replace([np.inf,-np.inf],np.nan)
C = B.cumprod()
D = C *100


#check = ((etf_price_data.sum(axis=0).subtract(etf_div_data.sum(axis=0),inplace=True,fill_value=0)).subtract(A.sum(axis=0)),inplace=True,fill_value=0)

check_2 = ((etf_price_data.sum(axis=0)-A.sum(axis=0)) - etf_div_data.sum(axis=0))
if check_2.sum().sum()>1:
    print 'Error'
else:
    print 'OK'
B_Check = (B-(etf_price_data.shift(1)/etf_price_data))
print 'B Check - ',B_Check.min(axis=0)

#replace column titles/order of columns in indices
#calculate overnight performance
#subtract TER/365

#replace nans in B with values from a B_Index
#screen B for nans, apply screen to B_Index
#B_Index is (today/yesterday)-daily TER

#adjust ETF/Indices in USD or EUR to GBP
'''



indices = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying Indices.csv',parse_dates='Date',dayfirst=True,index_col=['Date','Ticker'])

indices = indices.unstack()

indices = indices['Value']

indices = indices.ix[date_range]

indices.drop(['USDGBP Curncy','GBPEUR Curncy'],axis=1,inplace=True)

mapping = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Ticker-TER.csv')

indices_perf = indices/indices.shift(1)

B_index = indices_perf

B_index.drop(pd.datetime(2015,05,28),axis=0,inplace=True)

names = []

for name in B_index.columns:
    names.append(mapping.ETF[mapping.Index==name].values[0])

B_index.columns = names

mapping.index = mapping.ETF

B_index = B_index-(mapping.TER/365)

B_test = B.stack()

B_index_test = B_index.stack()

combined = pd.concat([B_index_test,B_test],axis=1,join='outer')

combined[1][combined[1].isnull()]=combined[0][combined[1].isnull()]

B_index = combined[1]

'''
'''
A.head(10)
B.head(10)
C.head(10)
C.tail(10)
B.tail(10)
B.drop('28/5/2015',inplace=True)
B.tail().index
B.tail(1).index
B.drop(B.tail(1).index,inplace=True)
B.tail()
C = B.cumprod()
C.tail()
B.head()
B.iloc[100:]
B.iloc[100:,:]
B.iloc[100,:]
B.iloc[635,:]
B.iloc[634,:]
B.iloc[633,:]
B.iloc[632,:]
B.iloc[631,:]
B.iloc[630,:]
B.iloc[628,:]
B.iloc[627,:]
B.replace([np.inf,-np.inf],np.nan)
import numpy as np
B.replace([np.inf,-np.inf],np.nan)
B.iloc[628,:]
B = B.replace([np.inf,-np.inf],np.nan)
B.iloc[628,:]
C = B.cumprod()
C.tail()
%run "C:/Users/Brandon mitchell/ARC Comparison/ARC_ETF_TR.py"
C.tail()
A = etf_price_data
B = etf_price_data/A.shift(1)
B.drop(B.tail(1).index,inplace=True)
B = B.replace([np.inf,-np.inf],np.nan)
C = B.cumprod()
D = C *100
C.tail()
indices = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying Indices.csv',parse_dates='Date',dayfirst=True)
indices.head(2)
indices = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying Indices.csv',parse_dates='Date',dayfirst=True,index_col=['Date','Ticker'])
indices.head(2)
indices = indices.unstack()
indices.head(2)
indices = indices['Value']
date_range
indices = indices[date_range]
indices = indices.ix[date_range]
indices.head(3)
indices.index.freq
indices.drop(['USDGBP Curncy','GBPEUR Curncy'],axis=1,inplace=True)
indices.head(3)
mapping = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Ticker-TER.csv')
mapping.head(2)
indices.shift(1).head(2)
indices_perf = indices/indices.shift(1)
indices_perf.head(2)
B_index = indices_perf
B_index.shape
B.shape
B_index.tail()
B.tail()
B.isnull
B_index.drop(pd.datetime(2015,05,28),axis=0,inplace=True)
B_index.shape
B.shape
B.isnull()
B[B.isnull()] = B_index[B.isnull()]
B_index[B.isnull()]
B_index.ix[B.isnull()]
B_index.head(2)
B.head(2)
B = B.Value
B_index[B.isnull()]
B_index.head(2)
B.head(2)
B.isnull()
B[B.isnull()]
B_index[B.isnull()]
B_index[~B.isnull()]
B.notnull()
B[B.notnull()]
test = B_index[B.isnull()]
test.tail()
test = B_index[~B.isnull()]
test.tail()
B[pd.isnull(B)]
B[~B]
B.mask(B.isnull())
B_index.head(2)
mapping.head(2)
for name in B_index.columns:
    B_index.rename({name:mapping.ETF[name]},inplace=True)
mapping.ETF['BCOMTR Index']
mapping.ETF
for name in B_index.columns:
    B_index.rename({name:mapping.ETF[mapping.Index[name]]},inplace=True)
mapping.ETF[mapping.Index['BCOMTR Index']]
mapping.Index['BCOMTR Index']
mapping.Index.ix['BCOMTR Index']
mapping.ix['BCOMTR Index']
mapping.loc['BCOMTR Index']
mapping.head(2)
mapping.Benchmark['BCOMF3T']
mapping.Benchmark=='BCOMF3T'
for name in B_index.columns:
    B_index.rename({name:mapping.ETF[mapping.Index==name]},inplace=True)
B_index.head(2)
for name in B_index.columns:
    print mapping.ETF[mapping.Index==name]
for name in B_index.columns:
    print mapping.ETF[mapping.Index==name][0]
for name in B_index.columns:
    print mapping.ETF[mapping.Index==name].value()
for name in B_index.columns:
    mapping.ETF[mapping.Index==name]
for name in B_index.columns:
    a = mapping.ETF[mapping.Index==name]
for name in B_index.columns:
    print a = mapping.ETF[mapping.Index==name]
for name in B_index.columns:
    a = mapping.ETF[mapping.Index==name]
    print a
for name in B_index.columns:
    a = mapping.ETF[mapping.Index==name]
    print type(a)
for name in B_index.columns:
    a = mapping.ETF[mapping.Index==name]
    print a.values
for name in B_index.columns:
    a = mapping.ETF[mapping.Index==name]
    print a.values[0]
for name in B_index.columns:
    B_index.rename({name:mapping.ETF[mapping.Index==name].values[0]},inplace=True)
B_index
for name in B_index.columns:
    mapping.ETF[mapping.Index==name].values[0]
for name in B_index.columns:
    print mapping.ETF[mapping.Index==name].values[0]
for name in B_index.columns:
    print {name:mapping.ETF[mapping.Index==name].values[0]}
B_index.rename({'BCOMTR Index': 'COMF LN Equity'})
B_index.rename({'COMF LN Equity':'BCOMTR Index'})
B_index.columns
names = []
for name in B_index.columns:
    names.append(mapping.ETF[mapping.Index==name].values[0])
names
B_index.columns = names
B_index.head(2)
B.head(2)
mapping.head(2)
mapping.index = mapping.ETF
mapping.head(2)
mapping.TER.shape
B_index.shape
B_index = B_index-mapping.TER
B_index.head()
B.head()
B_index_test = B_index.stack()
B_test = B.stack()
B_index_test.head(2)
B_test[B_test.isnull()]
B_index_test_2 = B_index_test[B_test.notnull()]
B_index_test.shape
B_test.shape
B_index_test[~B_test.index]
B_index_test[B_test.index]
B_index_test.isin(B_test.index)
B_index_test.all(B_test.index)
pd.merge(B_index_test,B_test,how='left')
B_test = pd.DataFrame(B_test)
B_index_test = pd.DataFrame(B_index_test)
B_index_test.merge(B_test,how='left')
B_test = B.stack()
B_index_test = B_index.stack()
pd.concat([B_index_test,B_test],axis=1,join='Outer')
pd.concat([B_index_test,B_test],axis=1,join='outer')
combined = pd.concat([B_index_test,B_test],axis=1,join='outer')
combined[1][combined[1].isnull()]==combined[0][combined[1].isnull()]
combined.head(2)
combined.head(10)
combined[1]
combined[1].isnull()
combined[0][combined[1].isnull()]
combined[1][combined[1].isnull()]=combined[0][combined[1].isnull()]
combined.head(2)
B_index = combined[1]
%history
B_index.head(2)
indices = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying Indices.csv',parse_dates='Date',dayfirst=True,index_col=['Date','Ticker'])

indices = indices.unstack()

indices = indices['Value']

indices = indices.ix[date_range]

indices.drop(['USDGBP Curncy','GBPEUR Curncy'],axis=1,inplace=True)

mapping = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison Data\Ticker-TER.csv')

indices_perf = indices/indices.shift(1)

B_index = indices_perf

B_index.drop(pd.datetime(2015,05,28),axis=0,inplace=True)

names = []

for name in B_index.columns:
    names.append(mapping.ETF[mapping.Index==name].values[0])

B_index.columns = names

mapping.index = mapping.ETF

B_index = B_index-(mapping.TER/365)

B_test = B.stack()

B_index_test = B_index.stack()

combined = pd.concat([B_index_test,B_test],axis=1,join='outer')

combined[1][combined[1].isnull()]=combined[0][combined[1].isnull()]

B_index = combined[1]
B_index.head(2)
B_index.shape
B_test.shape
combined.head(2)
B_index = B_index.unstack()
B_index.head()
C_combined = B_index.cumprod()
C_combined.tail()
C_combined = C_combined*100
C_combined.to_csv('P:\My Documents\ETFIndexCombined.csv')
%history
'''