"""Needs docstring!
"""

import pandas as pd
import numpy as np
#imports funds data


def import_funds(address):
    """Needs docstring!
    """
    funds_address = address
    funds = pd.read_csv(funds_address)
    funds = edit_column_names(funds)
    return funds


def edit_column_names(dataframe):
    """Needs docstring!
    """
    #takes n/ out of column names
    columns = dataframe.columns
    new_columns=[]
    for column in columns:
        column = column.replace('\n','').replace('\r','')
        new_columns.append(column)
    dataframe.columns = new_columns
    return dataframe


def rank_by_AUM(dataframe):
    """Needs docstring!
    """
    #gets Fund Size EUR from str to float
    dataframe['Fund Size EUR']=dataframe['Fund Size EUR'].map(lambda x: float(x.replace(',','')) if isinstance(x,str) else float(x))
    dataframe.sort('Fund Size EUR',ascending=False,inplace=True)
    #dataframe['Fund Size EUR'].map(lambda x: float(x))
    grouped = dataframe.groupby('Fund Size EUR',as_index=False).sum()
    grouped.sort('Fund Size EUR',ascending=False,inplace=True)
    grouped['Rank'] = np.arange(1,len(grouped)+1)
    ranking = grouped[['Fund Size EUR','Rank']]
    ranked = dataframe.merge(ranking,how='right',on='Fund Size EUR')
    return ranked    


def select_percentile(dataframe,percentile):
    """Needs docstring!
    """
    grouped = dataframe
    total = grouped['Fund Size EUR'].sum()
    grouped['Proportion'] = grouped['Fund Size EUR'].map(lambda x: x/total)
    grouped['Cum Proportion']=grouped.Proportion.cumsum()
    group = grouped[grouped['Cum Proportion']<percentile]
    return group


def choose_share_class(dataframe):
    """not working!
    """
    #sets variables for commonly used column names
    rank = 'Rank'
    fee = 'Management Fee'
    ter = 'Annual Report Net Expense Ratio'
    ongoing_charge = 'Annual Report Ongoing Charge'
    income = 'Distribution Status'
    #finds unique fund indentifiers in rank column
    ranks = pd.unique(dataframe[rank])
    #sets the boolean column to 0
    dataframe['Chosen Share Class'] = 0
    #sets a column to record difference from the target MER of .75
    dataframe['Difference'] = 0
    #loops through the fund identifiers
    for r in ranks:
        print 'Rank - ', r
        fund = dataframe[dataframe[rank]==r].copy()
        income_type = pd.DataFrame(pd.unique(dataframe[income]))
    #sorts out funds without accumulating share classes
        if income_type.isin(['Acc']).sum()[0] == 0:
            fund['Chosen Share Class'] = 'No Acc'
            print 'No Acc'
        else:        
            fund_acc = fund[fund[income]=='Acc'].copy()
            for row in np.arange(len(fund_acc)):
                if fund_acc['Management Fee'].iloc[row,]!="":
                    fund_acc['Difference'].iloc[row,] = np.absolute(\
                        fund_acc['Management Fee'].iloc[row,]-.75)
                    print 'Difference - ',fund_acc['Difference'].iloc[row,]
                else:
                    fund_acc['Chosen Share Class'].iloc[row,] = 'No MER'
                    print 'No MER'
            try:
                minimum = fund_acc['Difference'].min()
                print 'Minimum - ',minimum
                fund_acc['Chosen Share Class'][fund_acc['Difference']==minimum] = 1
                print 'Success'
                if len(fund_acc[fund_acc['Chosen Share Class']==1])>1:
                    acc = fund_acc[fund_acc['Chosen Share Class']==1].copy()
                    for row in np.arange(len(acc)):
                        print 'Row - ', row
                        print 'Name - ', acc['Name'].iloc[row,]
                        print 'MER - ', acc[fee].iloc[row,]
                    result = int(raw_input('Pick one!: '))
                    acc['Chosen Share Class'] = 0
                    acc['Chosen Share Class'].iloc[result,]=1
                    fund_acc[fund_acc['Chosen Share Class']==1] = acc
            except:
                result = 'error'
                fund_acc['Chosen Share Class'] = result
                print result
            fund[fund[income]=='Acc'] = fund_acc
        dataframe[dataframe[rank]==r] = fund
    return dataframe

