# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime

def month_string_to_number(string):
    m = {
        'jan':1,
        'feb':2,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
        }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

def years_conv(years):
    new_year=[]
    for year in years:
        prefix = year[:2]
        postfix =year[2:]
        pcs    = postfix.split('-')
        year1= prefix + pcs[0]
        new_year.append(year1)
#        year2= prefix + pcs[1]
#        new_year.append(year2)
    return new_year  


def year_conv(year):
    prefix = year[:2]
    postfix =year[2:]
    pcs    = postfix.split('-')
    year1= prefix + pcs[0]
    return year1

def timeseries(data, months):
    newdate=[]
    newdata=[]
    newyear=[]
    for idx1, rfrows in data.iterrows():
        year = year_conv(rfrows['YEAR'])
        for month in months:
            d ='1'
            mnt =month_string_to_number(month)
            newdate.append("-".join((year,str(mnt),d))) 
            newdata.append(rfrows[month]) 
            newyear.append(year) 
    
    dfdata = {'Data': newdata,'Datetime': newdate,'Year':newyear}        
    df = pd.DataFrame(dfdata)  
    df['Data'] = df['Data'].fillna(0)
    df = df[['Datetime','Year','Data']]    
    df['Datetime'] = pd.DatetimeIndex(df['Datetime']).floor('d')
#    df.set_index('Datetime', inplace=True)
    df.index =df['Datetime']
    df.index = df.index.to_period('m')
    idx = pd.date_range('1966-01-01','2012-01-01',freq='M').to_period('m')  
    #reindex and add NaN
    o_d = df.reindex(idx,fill_value=0)
    #filling missing date    
    #change periodindex to datetimeindex
    o_d['Datetime'] = o_d.index.to_timestamp()
    year_month =o_d['Datetime']
    o_d['Year'], o_d['Month'],o_d['Day'] = o_d['Datetime'].dt.year, o_d['Datetime'].dt.month,o_d['Datetime'].dt.day
    o_d['Datetime'] = pd.DatetimeIndex(year_month).floor('d')
    o_d = o_d[['Datetime','Year','Month','Day','Data']] 
    return o_d

def timeseries_sec(data, months):
    newdate=[]
    newdata=[]
    newyear=[]
    for idx1, rfrows in data.iterrows():
        year = rfrows['Year']
        for month in months:
            d ='1'
            mnt =month_string_to_number(month)
            newdate.append("-".join((str(year),str(mnt),d))) 
            newdata.append(rfrows[month]) 
            newyear.append(year) 
    
    dfdata = {'Data': newdata,'Datetime': newdate,'Year':newyear}        
    df = pd.DataFrame(dfdata)  
    df['Data'] = df['Data'].fillna(0)
    df = df[['Datetime','Year','Data']]    
    df['Datetime'] = pd.DatetimeIndex(df['Datetime']).floor('d')
#    df.set_index('Datetime', inplace=True)
    df.index =df['Datetime']
    df.index = df.index.to_period('m')
    idx = pd.date_range('1985-01-01','2012-01-01',freq='M').to_period('m')  
    #reindex and add NaN
    o_d = df.reindex(idx,fill_value=0)
    #filling missing date    
    #change periodindex to datetimeindex
    o_d['Datetime'] = o_d.index.to_timestamp()
    year_month =o_d['Datetime']
    o_d['Year'], o_d['Month'],o_d['Day'] = o_d['Datetime'].dt.year, o_d['Datetime'].dt.month,o_d['Datetime'].dt.day
    o_d['Datetime'] = pd.DatetimeIndex(year_month).floor('d')
    o_d = o_d[['Datetime','Year','Month','Day','Data']] 
    return o_d
    
