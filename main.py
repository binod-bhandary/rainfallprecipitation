#read excel files
import pandas as pd
import numpy as np
from functions import *

#==============================================================================
# defining variables
#==============================================================================
columns=['S.No.','YEAR','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER']
months=['JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER']
startrf = [0,48,97,147,195,243,292,341,394,0]
endrf = [44,93,142,191,240,288,336,386,438,0]

#==============================================================================
# import three excel files
#==============================================================================
cordff = pd.read_excel('./Data/Coordinates.xlsx', sheet_name='Sheet1')
rainfall_data = pd.read_excel('./Data/Precipitation - 9 stations - monthly.xlsx', sheet_name=0, skiprows=6,)
#rainfall_data2 = pd.read_excel('./Data/Precipitation - Zeerapur & Susaner  - Fortnightly.xlsx', sheet_name=0, skiprows=5)

#==============================================================================
# filling values for cordinates
#==============================================================================
stations_name = cordff['Station name']
cordff =cordff.append({'Station name':'Shajapur'},ignore_index=True)
cordff.set_index('Station name', inplace=True)
cordff.columns= ['lat','laval','lon','lovol'] 
cordff.loc['Shajapur', 'lat'] = 'Lat'
cordff.loc['Shajapur', 'lon'] = 'lon'


for col in cordff.columns:
    for idx, rows in cordff.iterrows():
        if pd.isnull(cordff.loc[idx,col]):
           cordff = cordff.fillna(cordff.mean()) 
        cdata = pd.DataFrame(rows).T
        cdata.to_csv('./StationsDataCsv/'+str(idx)+'.csv', index=False,header=False, sep=';')   
           
#==============================================================================
# filling vlaues for stations first           
#==============================================================================

ranges =rainfall_data.groupby(['S.No.']).get_group(1)
for idx , rows in ranges.iterrows():
    end = idx+44;
    df_selected = rainfall_data.loc[idx:end]
    rainfall_data.loc[idx:end] = df_selected.fillna(df_selected.mean())

#==============================================================================
# assigning values to stations name    
#==============================================================================
i=0
for name in stations_name:
    rawData         = rainfall_data[columns].loc[startrf[i]:endrf[i]]
    csvData         = timeseries(rawData,months)
    csvData.to_csv('./StationsDataCsv/'+name+'.csv', index=False, mode='a',sep=';') 
    i=i+1

#==============================================================================
# read second file and filling datas
#==============================================================================
df = pd.read_excel('./Data/Precipitation - Zeerapur & Susaner  - Fortnightly.xlsx', sheet_name=0, skiprows=5)
df = df.drop(df.index[[0,-1]])
#renaming unnamed columns
new_columns = [df.columns[i-1] + "2" if df.columns[i].find("Unnamed") >= 0 else df.columns[i] for i in range(len(df.columns))]
#reindexing values
df.columns = new_columns
li = zip(df.columns[1::2],df.columns[2::2])
temp = pd.DataFrame({i :df[i]+df[j] for i,j in li})
ndf = pd.concat([temp,df['Year']],1)
columns1 = ['Year','June','Jul','Aug','Sep','Oct']
months1 = ['June','Jul','Aug','Sep','Oct']
rainfall_data1 = ndf[columns1]

ranges =rainfall_data1.groupby(['Year']).get_group(1985)
for idx , rows in ranges.iterrows():
    end = idx+27;
    rainfall_data1.loc[idx:end] = rainfall_data1.fillna(0)

stations_name1 = pd.DataFrame({
        'name':['Zeerapur','Susaner'],
        'start':[1,33],
        'end':[27,60],
        })
stations_name1.set_index('name', inplace=True)

for idx,name in rainfall_data1.iterrows():
    rawData         = rainfall_data1[columns1].loc[name['start']:name['end']]
    csvdata         = timeseries_sec(rawData,months1)



