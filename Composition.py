'''
The objective of the code in this module is to calculate 
an ARC TAA Index/Fund from allocation data
'''

import pandas as pd
import numpy as np

class IndexData:
    
    def __init__(self,address):
        '''
        takes the csv file address
        uploads into a dataframe 'index_init'
        parses Date column
        sets Ticker and Date columns to index
        unstacks and filters to return 2D df of values
        sets to self.data
        '''
        self.address = address
        index_init = pd.read_csv(self.address, parse_dates='Date')  
        index_init.Date = pd.to_datetime(index_init.Date,format="%d/%m/%Y",dayfirst=True)
        index_data = index_init
        index_data.set_index(['Date','Ticker'],inplace=True)
        index_data_values = index_data.unstack().Value
        self.data = index_data_values

    def dropcurrencies(self):
        self.gbpeur = self.data.loc[:,'GBPEUR Curncy']
        self.gbpusd = self.data.loc[:,'USDGBP Curncy']
        self.data.drop(['GBPEUR Curncy','USDGBP Curncy'],axis=1,inplace=True)
        
    def performance(self,period):
        '''
        Takes in a Dataframe with sequential datetime index
        Returns performance values on given periodicity
        '''
        shifted = self.data.shift(period)
        performance = (self.data-shifted)/shifted
        self.performance = performance + 1
        self.performance_cum = self.performance.cumprod()
                   
            
    def find_date_range(self,allocation_data,period):
        self.date_min = self.data.index.min()
        self.date_max = self.data.index.max()
        self.date_total_min = np.array([self.date_min,allocation_data.date_min]).max()
        self.date_total_max = np.array([self.date_max,allocation_data.date_max]).max()
        self.date_range = pd.date_range(self.date_total_min,self.date_total_max,freq=period)
        
        
class AllocationData:
    
    def __init__(self,address):
        '''
        takes filepath
        uploads allocation data csv
        parses Implementation Date and Model Date columns
        sets index to Model Date, Implementation Date, Index
        sets data to self.data
        '''
        self.address = address
        allocation_init = pd.read_csv(self.address, parse_dates=['Implementation Date','Model Date'],dayfirst=True)
        self.data = allocation_init
        self.data.set_index(['Model Date','Implementation Date','Index'],inplace=True)
        
    def rename_columns(self,source_column,target_column,translation_table_address):
        translation_table = pd.read_csv(translation_table_address)
        a = self.data
        for x in a.columns:
            yo = translation_table[translation_table[source_column]==x][target_column].iloc[0]
            #print yo        
            a.rename_axis({x:yo},axis=1,inplace=True)
        self.data = a
        self.data.index = self.data.index.droplevel(0)
        self.data = self.data.stack()
        self.data = self.data.reorder_levels([0,2,1]).unstack().unstack()

    def set_date_range(self):
        '''
        Sets min and max dates in the allocation data
        '''
        self.date_min = self.data.index.get_level_values(0).min()
        self.date_max = self.data.index.get_level_values(0).max()
        self.date_range = pd.date_range(self.data.index.get_level_values(0).min(),
            self.data.index.get_level_values(0).max(),freq='D')
            
    def set_data_daily(self,period='D'):
        '''
        select resampling period
        default is businessday 'B'
        '''
        self.data_daily = self.data.resample(period,fill_method='ffill')
        #self.data_daily.fillna(value=1.0,inplace=True)
    
    def limit_date(self,index_data):
        '''
        limits the allocation table to dates inside index_data.date_range
        '''
        self.data_daily = self.data_daily.truncate(before=index_data.date_total_min)

class TAA_Index:
    
    def __init__(self,allocation_data,index_data):
        self.allocation_data = allocation_data
        self.index_data = index_data
        
    
    def generate_index(self):
        index = pd.DataFrame(np.ones([len(self.index_data.date_range),
            len(self.allocation_data.data.columns)]),columns=self.allocation_data.data.columns,
                index=self.index_data.date_range)
        index = index * 100.0
        self.index = index
    
    def calculate_indices(self):
        '''
        First Loop:
        Isolates the allocation data and taa_index for a single pci index
            as pci_data, pci_index
        
        Sets first row of pci_index as pci_data * 100
        
        Second Loop:    
        
        1. Picks out each row in pci_data individually, beginning with second row,
        2. Sets 'date' to the date of that row
        3. Finds corresponding date/row in pci_index
        4. Copies pci_index down to that date
        5. Multiplies pci_index by .performance_cum
        6. Rebalances index by:
            summing pci_index row as sum
            setting pci_index row to sum*row

        '''
        self.index_calc = pd.DataFrame(index = self.index_data.date_range,
            columns=pd.unique(self.allocation_data.data.columns.get_level_values(0)))
        
        self.final_index = pd.DataFrame(index = self.index_data.date_range,
            columns=pd.unique(self.allocation_data.data.columns.get_level_values(0)))
        
        for pci in pd.unique(self.allocation_data.data.columns.get_level_values(0)):
            
            pci_allocation = self.allocation_data.data_daily[pci]
            pci_index = self.index[pci]
            #multiply cumulative performances times weights and sum
            
            pci_index = self.calculate_underlying(pci_allocation,pci_index)
            #Sets final(ish) index values; compensates for something funky at the beginning
            #Starting value is 91.7 for balanced; should be 100
            #pci_index_perf = (pci_index/pci_index.shift(1))*100
            
            self.index_calc[pci] = pci_index/pci_index.shift(1)
            pci_index_calc = self.index_calc[pci]
            #goes period by period and carries index value forward
            start_value = 100
            for period in self.periods:
                pci_index_calc.ix[period] = pci_index_calc.ix[period]*start_value
                start_value = pci_index_calc.ix[period[-1]]
            self.final_index[pci] = pci_index_calc
            
    def calculate_underlying(self,pci_allocation,pci_index):
        performance = self.index_data.performance_cum
        index = pci_index*performance
        index = index*pci_allocation
        index_sum = index.sum(axis=1)
        return index_sum

    def crunch_periods(self):
        dates = self.allocation_data.data.index
        periods = []
        for date in np.arange(len(dates)-1):
            period = pd.date_range(dates[date],dates[date+1])
            periods.append(period)
        self.periods = periods
        #needs to drop the portion of the first period for which I don't have index data
        self.drop_periods = pd.date_range(self.allocation_data.date_min,
            self.index_data.date_min)
        self.periods[0] = self.periods[0].drop(self.drop_periods)



        
                
'''
calculate index
'''


#initial rebalance
#apply performance
#rebalance
#apply performance

#three items, taa_index, allocations, index_performance
#mask allocations and index performance by the minimum of taa_index
#index performance - index_performance
#test - taa_index
#cautious - allocations

#index_data.taa_index.iloc[0,:] = index_data.taa_index.iloc[0,:]*allocation_data.data.iloc[0,:]

#run loop; match date;

#for x in np.arange(len(test)):
#for y in np.arange(len(allocation_data)):
        