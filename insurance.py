from scipy.io import arff
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

## Load Data
data = arff.loadarff('Project_Learning.arff')

## Transform into Pandas Dataframe
df = pd.DataFrame(data[0])

## decode object columns into String
for cols in df.columns[df.dtypes == object]:
    df[cols] = df[cols].str.decode('utf-8')

## Map yes/no to 0/1
df["med"] = df["med"].map(dict(yes=1, no=0))
df["allergy"] = df["allergy"].map(dict(yes=1, no=0))
df["class"] = df["class"].map(dict(low=0, medium=1, high=2))

## Encode "disease" column into hot columns
df = pd.concat([df, pd.get_dummies(data=df["disease"])], axis=1)
df.drop(["disease", "no"], axis=1, inplace=True)

## print column datatype
for col in df.columns:
    print(col, df[col].dtype)

## Setup Train and test dataset
train_data = df.sample(frac=0.8, random_state=0)
test_data = df.drop(train_data.index)

## Show plot
#plot = sns.pairplot(train_data[["age", "bmi", "cholesterol", "diabetes", "heart", "class"]], diag_kind="kde")
#plt.show()

## Show overall statistics
#print(train_data.describe().transpose())

## Prepare training/label data
train_features = train_data.copy().astype("float32")
train_labels = train_features.pop("class")

test_features = test_data.copy().astype("float32")
test_labels = test_features.pop("class")

#normalizer = preprocessing.Normalization(input_shape=[9, ])
#normalizer.adapt(np.array(train_features))
#print(normalizer.mean.numpy())

model = keras.Sequential([
    keras.layers.Dense(18, activation="relu", input_shape=[9]),
    keras.layers.Dense(36, activation="relu"),
    keras.layers.Dense(18, activation="relu"),
    keras.layers.Dense(3, activation="softmax")
])
optimizer = keras.optimizers.Adam()
#optimizer = keras.optimizers.RMSprop(0.0099)
model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics="accuracy")
model.fit(x=train_features, y=train_labels, batch_size=16, epochs=1000,
          validation_split=0.2, shuffle=True)
