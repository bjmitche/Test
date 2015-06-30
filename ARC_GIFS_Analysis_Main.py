"""
This script is meant to provide access to all of the analytics to be run on the
GIFS universe of funds vs. the ARC products.

command line syntax
environment variables
environment files
"""

import pandas as pd
import numpy as np

import ARC_GIFS_Analysis as aga
import Sorting_GIF_Peers as sgp

"""
Data imports
"""
import_command = raw_input("Import Data? Yes/No: ")
if import_command == "Yes":
    #Imports GIFS NAV data
    nav_address = ('P:\My Documents\Steering\ARC\PCI and Comparison Data\Peer '
                    'Group Data\90% Subset NAVs.csv')
    navs = aga.import_navs(nav_address)
    print "NAV data imported - "+nav_address[-20:]
    #Imports ARC time series data
    indices_address = ('P:\My Documents\Steering\ARC\PCI and Comparison Data'
                        '\Revised TAA Data\Revised Indices.csv')
    arc = aga.import_arc_data(indices_address)
    print "ARC data imported - "+indices_address[-25:]
    #Imports table of static data for GIFS universes
    funds_address = ('P:\My Documents\Steering\ARC\PCI and Comparison Data'
                    '\Peer Group Data\GIFS GBP Multiasset Funds.csv')
    funds = sgp.import_funds(funds_address)
    #Imports a set of preferred share classes
    chosen_funds = pd.read_csv('P:\My Documents\Steering\ARC\PCI and Comparison'
                            ' Data\Peer Group Data\ChosenFunds 15.6.csv')

"""Establish top 90% of funds by AUM
Establish set of Acc share classes
Establish Acc share classes of top 90% funds
"""
slice_command = raw_input("Rank and Slice? Yes/No: ")
if slice_command == 'Yes':
    
    funds = sgp.rank_by_AUM(funds)
    top_ninety = sgp.select_percentile(funds,.9)
    
    acc_funds = funds[funds['Distribution Status']=='Acc']
    top_ninety_acc = top_ninety[top_ninety['Distribution Status']=='Acc']
    
    top_ninety_navs = navs[top_ninety.ISIN[top_ninety.ISIN.notnull()]]
    acc_navs = navs[acc_funds.ISIN[acc_funds.ISIN.notnull()].get_values()]
    top_ninety_acc_navs = navs[top_ninety_acc.ISIN[top_ninety_acc.ISIN_
                                                  .notnull()]]
    
    total_top_navs = pd.concat([arc,top_ninety_navs],axis=1)
    total_top_acc_navs = pd.concat([arc,top_ninety_acc_navs],axis=1)
    
    #Total share classes in result set
    print 'Total Share Classes - ',len(funds)
    #Total funds in result set
    print 'Total Funds w. AUM - ',funds.Rank.max()
    #Total listings in top 90%
    print 'Top 90% Share Class Count - ',len(top_ninety)
    #Total funds in top 90%
    print 'Top 90% Funds w. AUM - ',top_ninety.Rank.max()
    #Total funds with Acc share classes
    print 'Total Funds with Acc Share Classes - ', \
        len(pd.unique(acc_funds.Rank))
    #Total top 90% funds with Acc share classes
    print 'Total Top 90% Acc Funds - ', len(pd.unique(top_ninety_acc.Rank))






"""
Main Task #1
Check and Sort Data
"""


"""
Main Task #2
Run Calculations
Discreet Periods
A1. Performance
B1. Volatility
C1. Ratio
Rolling Periods
A2. Performance
B2. Volatility
C2. Ratio
D. Drawdown
E. AUM by Bucket
F. AUM vs. Inception Date
"""
#A1-C1

all_data = aga.PanelData(total_navs)
all_data.ratio()
#all_data.ranking_peers()
#all_data.percentiles()
all_data.relative_vol()
all_data.relative_vol_data_buckets()

for x in all_data.arc_bands:
    x = x.replace(' ','_')
    a = getattr(all_data,x+'_mask')
    all_data.ranking_peers(a,x)

for x in all_data.arc_bands:
    x = x.replace(' ','_')
    all_data.percentiles(x)
all_data.ranking_peers(all_data.Main,'main')
all_data.percentiles('main')

#D

def rolling_relative_vol(all_data,relevant_labels,perf_period,vol_period):
    arc_data = all_data.navs[relevant_labels]
    arc_perf = arc_data.pct_change(perf_period)
    arc_vol = pd.rolling_std(arc_perf,vol_period,vol_period)
    rel_vol = arc_vol/arc_vol['MSCI World']
    print 'Mean',rel_vol.mean(axis=0)
    print 'STD',rel_vol.std(axis=0)
    return rel_vol

'''
Main Task #3
Check Calculations
'''

'''
Main Task #4
Data Display
'''
relevant_lables = all_data.navs.columns[:8]

a = all_data.Balanced_perc.Performance.loc[relevant_lables].transpose().stack()
b = all_data.Steady_Growth_perc.Performance.loc[relevant_lables].transpose().stack()
c = all_data.Equity_Risk_perc.Performance.loc[relevant_lables].transpose().stack()
a= pd.DataFrame(a)
b= pd.DataFrame(b)
c= pd.DataFrame(c)
a['Bucket'] = 'Balanced'
b['Bucket'] = 'Steady Growth'
c['Bucket'] = 'Equity Risk'
performance = pd.concat([a,b,c],axis=0)


a = all_data.Balanced_perc.Ratio.loc[relevant_lables].transpose().stack()
b = all_data.Steady_Growth_perc.Ratio.loc[relevant_lables].transpose().stack()
c = all_data.Equity_Risk_perc.Ratio.loc[relevant_lables].transpose().stack()
a= pd.DataFrame(a)
b= pd.DataFrame(b)
c= pd.DataFrame(c)
a['Bucket'] = 'Balanced'
b['Bucket'] = 'Steady Growth'
c['Bucket'] = 'Equity Risk'
ratio = pd.concat([a,b,c],axis=0)

