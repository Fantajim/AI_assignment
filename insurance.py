from scipy.io import arff
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from time import time
import json

## Data time

# Initialize Scaler
scaler = MinMaxScaler()

# Load Data
data = arff.loadarff('Project_Learning.arff')

# Transform into Pandas Dataframe
df = pd.DataFrame(data[0])

# decode object columns into String
for cols in df.columns[df.dtypes == object]:
    df[cols] = df[cols].str.decode('utf-8')

# Map yes/no to 0/1
df["med"] = df["med"].map(dict(yes=1, no=0))
df["allergy"] = df["allergy"].map(dict(yes=1, no=0))

# Map "class" label to integer
df["class"] = df["class"].map(dict(low=0, medium=1, high=2))

# Encode "disease" column into hot columns
df = pd.concat([df, pd.get_dummies(data=df["disease"])], axis=1)
# disease column is no longer needed because its hot encoded into columns
df.drop(["disease", "no"], axis=1, inplace=True)

# Setup Train and test dataset
train_data = df

# Prepare training/label data
train_features = train_data.copy()
train_labels = train_features.pop("class")

train_features = train_features.astype(float)

# [OPTIONAL]Show overall statistics
#print(train_features.describe().transpose())

# Normalize features so that they are between 0 and 1
train_features = pd.DataFrame(scaler.fit_transform(train_features), columns=train_features.columns)

# [OPTIONAL] Show plot
#plot = sns.pairplot(train_data[["age", "bmi", "cholesterol", "diabetes", "heart", "class"]], diag_kind="kde")
#plt.show()

## Model time

# Initialize and configure EarlyStopper
early_stop = EarlyStopping(monitor='val_loss', patience=10)

model = keras.Sequential([
    keras.layers.Dense(18, activation="relu", input_dim=train_features.shape[1]),

    keras.layers.Dense(36, activation="relu"),
    keras.layers.Dropout(0.2),

    keras.layers.Dense(8, activation="relu"),

    keras.layers.Dense(3, activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics="accuracy")

# Setup callback -> to stop when model starts to overfit. Thats why we can mostly ignore the high epoch amount
trained_model = model.fit(x=train_features, y=train_labels, batch_size=8, epochs=500,
                          validation_split=0.2, shuffle=True, verbose=1, callbacks=[early_stop])
folder_name = f"./model{time()}"
data = {}
data['accuracy'] = trained_model.history['accuracy']
data['val_accuracy'] = trained_model.history['val_accuracy']
data['loss'] = trained_model.history['loss']
data['val_loss'] = trained_model.history['val_loss']

model.save(filepath=folder_name)
with open(f"{folder_name}/model_history.txt", "w") as out:
    json.dump(data, out)

## Plotting time

# accuracy plot
"""plt.plot(trained_model.history['accuracy'])
plt.plot(trained_model.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# loss plot
plt.plot(trained_model.history['loss'])
plt.plot(trained_model.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Print the final model values
print("last validation accuracy: ",trained_model.history['val_accuracy'][-1:])
print("last validation loss: ",trained_model.history['val_loss'][-1:], "\n")"""
model.summary()