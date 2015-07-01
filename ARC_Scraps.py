"""
Fund launch by year
"""
a = pd.to_datetime(chosen_funds['Inception Date'],dayfirst=True)
chosen_funds['Inception Date'] = a

dates = chosen_funds.groupby('Rank').min()
dates.index = dates['Inception Date']
dates['Count'] = 1
yo = dates['Count','Fund Size EUR']
by_year = yo.resample('BA-May',how='sum')

a = "asdfaoudf"

"""
Chchanges
"""