import geopandas
import matplotlib.pyplot as plt
import pandas as pd

filename_map = "data/Planning_Districts.geojson"
filename_crimes = "data/crime_boston.csv"

file_map = open(filename_map)
df_crimes_raw = pd.read_csv(filename_crimes, encoding='utf8', sep=';')

df_crimes_raw = df_crimes_raw.drop(df_crimes_raw[df_crimes_raw['Lat'] != 0])

df_map = geopandas.read_file(file_map)
df_crimes = geopandas.GeoDataFrame(df_crimes_raw,
                             geometry=geopandas.GeoSeries.from_xy(df_crimes_raw['Long'], df_crimes_raw['Lat']),
                             crs=4326)

print(df_map.head())
df_map.plot(column='PLANNING_D')
df_crimes.plot(marker='*', color='green', markersize=5);
plt.show()