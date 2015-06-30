"""
ARC Monthly Peer Analysis
"""

import pandas as pd
import numpy as np

class PanelData:
    """Storage for input of NAVs and output of precentile rankings
    
    """
    def __init__(self,concat):
        """Store NAV Values; Ensure that NaNs are ffilled."""
        self.navs = concat
        self.navs.fillna(method='ffill',inplace=True)
    
    def discrete_annualized_performance(self):
        """Calculate annualized performance over 1 through 10 year periods."""
        navs = self.navs
        total_performance = pd.DataFrame()
        for x in np.arange(1,11):
            period = (12*x)+1
            nav_period = navs[-period:]
            performance = nav_period.pct_change(period-1)
            exp = (1.0/x)
            performance = ((performance[-1:]+1)**exp)-1
            total_performance = pd.concat([total_performance,performance],axis=0)
        total_performance.index = np.arange(1,11)
        return total_performance

    def volatility_func(self):
        """Calculate volatility over 1 through 9 year periods."""
        navs = self.navs
        period = 12
        total_vol = pd.DataFrame(index=navs.columns)
        for x in np.arange(1,11):
            period = 12*x
            #slices df to select the appropriate number of rows
            nav_start = navs.iloc[(len(navs)-(period)):(len(navs)),]
            n = nav_start/nav_start.shift(1)
            vol = n.std(axis=0,skipna=True)*np.sqrt(12)
            total_vol = pd.concat([total_vol,vol],axis=1)
        numbers = np.arange(1,11)
        total_vol.columns = numbers
        total_vol = total_vol.transpose()
        return total_vol

    def ratio(self):
        performance = self.discrete_annualized_performance()
        #why do I do this?
        self.perf = performance.transpose()
        volatility = self.volatility_func()
        self.vol = volatility.transpose()
        self.vol = self.vol[self.perf.notnull()]
        self.ratio = self.perf/self.vol
        #data = {'Performance':performance,'Volatility':volatility,'Ratio':ratio}
        #panel = pd.Panel(data)
        #return panel
        
    def relative_vol(self):
        self.msci_vol = self.vol.loc['MSCI World']
        relative_vol_raw = (self.vol/self.msci_vol)
        test = relative_vol_raw
        #10 is now completely nan
        test.drop(10,axis=1,inplace=True)
        self.arc_bands = {'Cautious':[0,.4],'Balanced':[.4,.6],'Steady Growth':[.6,.8],'Equity Risk':[.8,2]}
        for x in self.arc_bands:
            print x
            test[(test>self.arc_bands[x][0]) & (test<self.arc_bands[x][1])] = x
        self.relativevol = test
        
    def ranking_peers(self,mask,name):
        """Rank share classes by year."""
        perf = self.perf[mask]
        vol = self.vol[mask]
        ratio = self.vol[mask]
        perfranking = perf.rank(ascending=False,numeric_only=True)
        volranking = vol.rank(numeric_only=True)
        ratioranking = ratio.rank(ascending=False,numeric_only=True)
        data = {'Performance':perfranking,'Volatility':volranking,
                'Ratio':ratioranking}
        panel = pd.Panel(data)
        setattr(self,name+'_rank',panel)
    
    def percentiles(self,name):
        """Calculate rank percentiles."""
        rank = getattr(self,name+'_rank')
        perf_rank = rank.Performance
        vol_rank = rank.Volatility
        ratio_rank = rank.Ratio
        total_count = vol_rank.mean(axis=0)*2
        print name, total_count
        perf_percentile = (total_count - perf_rank)/total_count
        vol_percentile = (total_count - vol_rank)/total_count
        ratio_percentile = (total_count - ratio_rank)/total_count
        data = {'Performance':perf_percentile,'Volatility':vol_percentile,
                'Ratio':ratio_percentile}
        panel = pd.Panel(data)
        setattr(self,name+'_perc',panel)
        
    def relative_vol_data_buckets(self):
        """Return a df for each PCI bucket."""
        for bucket in self.arc_bands:
            v = self.relativevol==bucket
            bucket = bucket.replace(' ','_')
            setattr(self,bucket+'_mask',v)
        self.Main = self.Balanced_mask.applymap(lambda x: True)


def import_navs(address):
    """Imports and handles a csv file of BB NAV data for GIFS products"""
    nav_address = address
    navs = pd.read_csv(nav_address,parse_dates='Date',dayfirst=True,index_col='Date')
    #after this, all cells should be either float or NaN (Task 3)
    navs = navs.replace('#N/A Invalid Security',value=np.nan)
    navs = navs.replace('#N/A Requesting Data...',value=np.nan)
    navs.fillna(method='ffill',inplace=True)
    navs_num = navs.convert_objects(convert_numeric=True)
    return navs_num


def import_arc_data(address):
    """Imports time series values for ARC PCI and TAA Products
    Handles column names
    """
    indices_address = address
    indices = pd.read_csv(indices_address,parse_dates=['Business Date','Calendar Date'],dayfirst=True,index_col='Business Date')
    indices.drop('Calendar Date',inplace=True,axis=1)
    return indices
    
    
def import_inception_dates():
    inception_date_address = 'P:\My Documents\Steering\ARC\PCI and Comparison Data\Peer Group Data\GIFS Inception Dates.csv'
    inception_dates = pd.read_csv(inception_date_address,parse_dates='Inception Date',dayfirst=True,index_col='ISIN')
    #parse_dates above isn't working on inception_dates
    inception_dates['Inception Date'] = pd.to_datetime(inception_dates['Inception Date'],dayfirst=True)
    return inception_dates
    
    
"""
Could be deleted    
def my_function(x):
   if x<33 and x>=0:
        return True
   if x<0:
       return True
   else:
       return False
"""


def relative_vol_data_buckets(relvol,concat,arc_bands):
    """Return a df for each PCI bucket"""
    for bucket in arc_bands:
        all_data.vol[all_data.relativevol=='Balanced']
      
      
def max_dd(ser):
    """max2here is the 'maximum to date' for each date in the series
    dd2here is the difference between the value at that date and the maximum up
    to that date
    max_indexer picks out the relevant maximum date
    """
    max2here = pd.expanding_max(ser)
    dd2here = ser - max2here
    mindate = dd2here[dd2here==dd2here.min()].index[0]
    maxindexer = max2here[:mindate].max()
    maxvalue = max2here[max2here==maxindexer].iloc[0,]
    maxdate = max2here[max2here==maxindexer].index[0]
    dd = dd2here.min()/maxvalue
    return dd


def max_dd_date(ser):
    """max2here is the 'maximum to date' for each date in the series
    dd2here is the difference between the value at that date and the maximum up
    to that date
    max_indexer picks out the relevant maximum date
    """
    max2here = pd.expanding_max(ser)
    dd2here = ser - max2here
    mindate = dd2here[dd2here==dd2here.min()].index[0]
    maxindexer = max2here[:mindate].max()
    maxvalue = max2here[max2here==maxindexer].iloc[0,]
    maxdate = max2here[max2here==maxindexer].index[0]
    dd = dd2here.min()/maxvalue
    result = [maxdate,mindate]
    return result


def rolling_max_dd(series):
    """
    Takes a series object of time series values
    Applies rolling time frame
    Returns a series with max dd within rolling timeframe
    """   
    rolling_dd = pd.rolling_apply(s, 10, max_dd, min_periods=0)
    df = pd.concat([s, rolling_dd], axis=1)
    df.columns = ['s', 'rol_dd_10']
    return df


def dd_prep(all_data,years):
    for num in np.arange(1,years):
        df = all_data.navs[-(12*num):]
        print num
        print df.shape
        df_count = df.notnull().sum(axis=0)[~(df.notnull().sum(axis=0)<12*num)]
        df_rel = df[df_count.index]
        print df_count.shape
        print df_rel.shape
        print max_dd(df_rel)
        print max_dd(df_rel).rank(ascending=True,pct=True)

