'''
ARC GIFS Analysis
Spare Code
'''

#shift performance panels into single df


'''
def ranking_peers(concat):
    #rank share classes by year
    perf_ranking = concat.loc['Performance'].rank(ascending=False,numeric_only=True)
    vol_ranking = concat.loc['Volatility'].rank(numeric_only=True)
    ratio_ranking = concat.loc['Ratio'].rank(ascending=False,numeric_only=True)
    result = PanelData(perf_ranking,vol_ranking,ratio_ranking)
    return result
    
def percentiles(concat,ranking):
#calculate rank percentiles
    total_count = vol_ranking.mean(axis=0)*2
    perf_percentile = (total_count - perf_ranking)/total_count
    vol_percentile = (total_count - vol_ranking)/total_count
    ratio_percentile = (total_count - ratio_ranking)/total_count
'''
'''
arc_labels = total_arc.major_axis.get_level_values(0)

#calculate relative volatility buckets
msci_vol = concat.loc['Volatility']['MSCI World']
nav_vol = concat.loc['Volatility'].transpose()
relvol = aga.relative_vol(nav_vol,msci_vol)
'''





'''
#Funds with and without data (Task 1)
data_test = navs.idxmax(axis=0)
has_data = data_test[~data_test.isin([pd.NaT])]
no_data = data_test[data_test.isin([pd.NaT])]
#(Task 2) - is start date near or before inception date?
inception_dates['Inception Range']=inception_dates['Inception Date'].map(lambda\
    x: len(pd.date_range(x,navs.index.max(),freq='BM')))
inception_dates['Actual Range']=inception_dates['ISIN'].map(lambda x: navs[x]\
    .notnull().sum())


inception_dates['Acceptable Difference'] = inception_dates['Difference'].map(lambda x: my_function(x))
#(Task 4)
inception_dates['Years'] = inception_dates['Actual Range']//12
#funds w/3 years of performance
three_years = navs[inception_dates.ISIN[inception_dates.Years>=3].values.tolist()]
three_years_perf = three_years/three_years.shift(1)
'''
'''
ranges = pd.datetime(2000,02,5)-pd.datetime(2000,01,01)
data_points = navs.notnull().sum(axis=0)
'''
'''
for ISIN in data_points.index:
    print ISIN
    start_date = inception_dates['Inception Date'][inception_dates['ISIN']==ISIN].iloc[0,]
    print start_date
    print len(pd.date_range(start_date,navs.index.max(),freq='BM'))
'''

'''
for column in navs.columns:
    navs_date = navs[column][navs[column].notnull()].index.min()
    inception_date = inception_dates['Inception Date'][inception_dates['ISIN']==column]
    print column
    print navs_date
    print inception_date
    print navs_date-inception_date
'''
'''
g = lambda x: len(pd.date_range(inception_dates['Inception Date'][inception_dates['ISIN']==x].iloc[0,],navs.index.max(),freq='BM'))
inception_dates['Inception Range']=inception_dates['Inception Date'].map(lambda x: len(pd.date_range(x,navs.index.max(),freq='BM')))

for ISIN in data_points.index:
    print g(ISIN)
'''
'''
#calculate calendar year performance for checking with MS performance numbers
period = 6
for x in np.arange(1,4):
    nav_end = navs.iloc[len(navs)-(period),]
    nav_start = navs.iloc[len(navs)-(period+12),]
    performance = nav_end/nav_start
    period = period+a(1)
    print x
    print nav_start
    print nav_end
    print performance
'''



'''

panel_df = panel.to_frame()
arc_df = arc_data.to_frame()
concat = pd.concat([panel_df,arc_df],axis=0)
concat = concat.unstack()
ranking = test_concat.rank(ascending=False)
maximum = ranking.max(axis=0)
labels = arc_data.major_axis.get_level_values(0)
indices_results = ranking.loc[labels]
indices_percentile = (1-(indices_results/maximum))
'''