import os
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
from geopandas import GeoSeries, GeoDataFrame

from shapely.geometry import Point
import shapefile

data_pth = "./Data"



cordff = pd.read_excel('./Data/Coordinate_test.xlsx', sheet_name='Sheet1')
cordff.columns= ['name','lt','lat','ln','lon'] 

geometry = [Point(xy) for xy in zip(cordff['lon'], cordff['lat'])]
#drop the text columns for latitude and longitude, as they are now contained within the geometry column
cordff = cordff.drop(['lt','lat','ln','lon'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(cordff, crs=crs, geometry=geometry)
#gdf.plot(marker='*', color='red', markersize=50, figsize=(3, 3));

rainfall = gpd.read_file(os.path.join(data_pth, "KaliSindh_WGS84.shp"))
#rainfall.plot(cmap='Set2', figsize=(10, 10));

gdf.plot(ax=rainfall.plot(cmap='Set2', figsize=(10, 10)), facecolor='red');