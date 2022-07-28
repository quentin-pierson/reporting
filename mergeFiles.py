import pandas as pd
filename_map = "data/crime_boston.csv"
filename_join = "data/rmsoffensecodes_group.csv"
file_map = open(filename_map)
file_join = open(filename_join)
df1 = pd.read_csv(file_map, encoding='utf8', sep=';')
df2 = pd.read_csv(file_join, encoding='utf8', sep=',')

newfile = pd.merge(df1, df2, on="OFFENSE_CODE")

newfile.to_csv("data/crimes_boston_raffined.csv", index=False, encoding="utf_8")