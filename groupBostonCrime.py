import pandas
import pandas as pd

df = pd.read_csv("data/rmsoffensecodes.csv", delimiter=";", encoding="utf_!")

print(df.columns)

df = df.reset_index()
df = df.sort_values(by=['CODE'])

df2 = df.replace(" ", "-", regex=True)

df2['NAME'] = df2['NAME'].str.split('-')

print(df)
print(df.columns)

print("-------")
print(df2)

y = ""
j = 0
tab = []
for i in df2['NAME'].values:
    if y != i[0]:
        y = i[0]
        j += 1
    tab.append(j)

df["group"] = tab

print(df)

df.to_csv("data/rmsoffensecodes_group.csv", index=False, encoding="utf_8")
