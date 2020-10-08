from scipy.io import arff
import pandas as pd
import numpy as np

## Load Data
data = arff.loadarff('Project_Learning.arff')
## Transform into Pandas Dataframe
df = pd.DataFrame(data[0])

## decode object columns into String
for cols in df.columns[df.dtypes==object]:
    df[cols] = df[cols].str.decode('utf-8')

## Map yes/no to 0/1
df["med"] = df["med"].map(dict(yes=1, no=0))
df["allergy"] = df["allergy"].map(dict(yes=1, no=0))

## Encode "disease" column into hot columns
df = pd.concat([df, pd.get_dummies(data=df["disease"])],axis=1)
df.drop(["disease", "no"], axis=1, inplace=True)

## test column names
for col in df.columns:
    print(col, df[col].dtype)


print(df.head())
print(df.tail())
print(df.values)
