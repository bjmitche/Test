'''
Composition Main
'''

import Composition as cm


allocation_address = 'P:\My Documents\Steering\ARC\PCI and Comparison Data\ARC Allocations.csv'
index_data_address = 'P:\My Documents\Steering\ARC\PCI and Comparison Data\Underlying Indices.csv'
translation_table_address = 'P:\My Documents\Steering\ARC\PCI and Comparison Data\Relation_Table.csv'

index_data = cm.IndexData(index_data_address)

allocation_data = cm.AllocationData(allocation_address)
allocation_data.rename_columns('ETF_Name','Index_Ticker',translation_table_address)
allocation_data.set_date_range()
allocation_data.set_data_daily()

index_data.find_date_range(allocation_data,'D')
allocation_data.limit_date(index_data)
index_data.dropcurrencies()
index_data.performance(1)
taa_indices = cm.TAA_Index(allocation_data,index_data)
taa_indices.crunch_periods()
taa_indices.generate_index()


'''for row_loc in np.arange(len(allocation_data.data)):
    row = allocation_data.data.iloc[row_loc,:]
    date = row.name[0]'''
    