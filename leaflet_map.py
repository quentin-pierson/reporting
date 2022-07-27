import geopandas

filename = "data/Planning_Districts.geojson"
file = open(filename)
df = geopandas.read_file(file)
df.head()
df.plot()