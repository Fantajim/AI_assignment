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

# Map diseases to integers
df["disease"] = df["disease"].map(dict(no=0, cholesterol=1, diabetes=2, heart=3))

# Prepare training/label data
train_features = df.copy().astype("float32")
train_labels = train_features.pop("class")

# [OPTIONAL]Show overall statistics
#print(train_features.describe().transpose())

# [OPTIONAL] Show plot
#plot = sns.pairplot(train_data[["age", "bmi", "cholesterol", "diabetes", "heart", "class"]], diag_kind="kde")
#plt.show()

import json
import random
import os

options = ["Single", "Loop static Layers", "Loop and let RNGesus take the wheel", "Refine model"]
## Model time
##############################################################################################
### General setup parameters
## set desired mode
# option[0] will just generate and save a model with our default static layers in a single run
# option[1] will loop for the set amount of tries and find a better model, then save it
# option[2] will loop to find a better model... but every layer is random (pure chaos -> not efficent but interesting)
# option[3] will load the weights from the former best model and preloads a new model with them (must have same tensor structure)
#
# Change the mode here:
mode = options[1]

# Set the amount of trial runs (Ignored for option[0])
tries = 20

# Specify the path of the model folder (Edit this to an existing folder on your Google Drive)
folder_name = "best_insurance_model"

###Keras parameters
##Change the model parameters here
# layers (These are our default tensor values)
# -> layer parameters with 0/False are ignored by the model
layer1 = 7
layer2 = 14
layer3 = 0
dropout1 = 0
dropout2 = 0
dropout3 = 0
layer2_active = True
layer3_active = False
dropout1_active = False
dropout2_active = False
dropout3_active = False
flatten1_active = False
flatten2_active = False

# model fit
batch = 10
validation_split = 0.1
shuffle = True
callback_patience = 10

##############################################################################################

# Initialize and configure EarlyStopper
# Callback -> to stop when model starts to overfit. Thats why we can mostly ignore the high epoch amount we are gonna set
early_stop = EarlyStopping(monitor='val_loss', patience=callback_patience)


# Utility function to save model in Gdrive with history data in Json format
def save_model(trained_model, trained_model_history):
    # json save
    data = {}
    data['accuracy'] = trained_model_history.history['accuracy']
    data['val_accuracy'] = trained_model_history.history['val_accuracy']
    data['loss'] = trained_model_history.history['loss']
    data['val_loss'] = trained_model_history.history['val_loss']
    with open(f"{folder_name}/model_history.txt", "w") as out:
        json.dump(data, out)

    # model save
    trained_model.save(filepath=folder_name)


# Utility function to prepare and run models
def setup_model(weights=None):
    global layer1
    global layer2
    global layer3
    global dropout1
    global dropout2
    global dropout3
    global layer2_active
    global layer3_active
    global dropout1_active
    global dropout2_active
    global dropout3_active
    global flatten1_active
    global flatten2_active

    # Initialize Model
    model = keras.Sequential()

    # randomize tensors if options[2] is enabled
    if mode == options[2]:
        layer1 = random.randint(1, 100)
        layer2 = random.randint(1, 100)
        layer3 = random.randint(1, 100)
        dropout1 = random.uniform(0, 0.5)
        dropout2 = random.uniform(0, 0.5)
        dropout3 = random.uniform(0, 0.5)
        layer2_active = random.choice([True, False])
        layer3_active = random.choice([True, False])
        dropout1_active = random.choice([True, False])
        dropout2_active = random.choice([True, False])
        dropout3_active = random.choice([True, False])
        flatten1_active = random.choice([True, False])
        flatten2_active = random.choice([True, False])

    # define model

    # input layer with Flatten
    model.add(layers.Flatten(input_shape=train_features.shape[1:])),

    model.add(layers.Dense(layer1, activation="relu"))

    # All hidden layers below will get ignored if set to False in parameters or 0 for Dense/Dropout layers
    if dropout1_active and dropout1 > 0: model.add(layers.Dropout(dropout1))
    if flatten1_active: model.add(layers.Flatten())

    if layer2_active and layer2 > 0: model.add(layers.Dense(layer2, activation="relu"))
    if dropout2_active and dropout2 > 0: model.add(layers.Dropout(dropout2))
    if flatten2_active: model.add(layers.Flatten())

    if layer3_active and layer3 > 0: model.add(layers.Dense(layer3, activation="relu"))
    if dropout3_active and dropout3 > 0: model.add(layers.Dropout(dropout3))

    # Output layer
    model.add(layers.Dense(3, activation="softmax"))

    # Set weights from previous best model when options[3] is selected
    if mode == options[3]: model.set_weights(weights)

    # compile model
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics="accuracy")

    # fit model
    model_history = model.fit(x=train_features, y=train_labels, batch_size=batch, epochs=500,
                              validation_split=validation_split, shuffle=shuffle, verbose=0, callbacks=[early_stop])
    # return model and its history
    return model, model_history


## Start of application

# Check if model/history has already been created to check against, otherwise just create a single model
if mode != options[0] and (os.path.exists(f"{folder_name}/saved_model.pb") is False or os.path.exists(
        f"{folder_name}/model_history.txt") is False):
    print("There seems to be no model present to compare against.")
    print("Creating a single model before executing the chosen loop option...")
    trained_model, trained_model_history = setup_model()
    save_model(trained_model, trained_model_history)
    print("Model and its history are created, proceeding with selected loop option")

# Check if Single mode has been selected
if mode != options[0]:
    # open former json history file
    with open(f"{folder_name}/model_history.txt") as file:
        former_best_history = json.load(file)

    former_best_weights = None
    if mode == options[3]:
        former_best_model = keras.models.load_model(folder_name)
        former_best_weights = former_best_model.get_weights()

    for int in range(tries):
        # create a model and its history
        trained_model, trained_model_history = setup_model(former_best_weights)

        # Check if the created model has a lower validation loss than the stored one
        if former_best_history["val_loss"][-1] > trained_model_history.history["val_loss"][-1]:

            # Print the model validation loss along with a summary
            print(f"Found better model with a val_loss of {trained_model_history.history['val_loss'][-1]}")
            print(f"Found better model with a val_accuracy of {trained_model_history.history['val_accuracy'][-1]}")

            print(trained_model.summary())

            # Save the model/history to Gdrive
            save_model(trained_model, trained_model_history)

            # Update the current best history for the remaining loops
            with open(f"{folder_name}/model_history.txt") as file:
                former_best_history = json.load(file)

        else:
            print(f"no luck.. Throwing the dice again")

else:
    trained_model, trained_model_history = setup_model()
    save_model(trained_model, trained_model_history)

## Plotting time

#[OPTIONAL] Enable and specify folder path to load a model outside of the default folder or if Model code has not been run yet
#folder_name = "best_insurance_model"

#Read data from the model folder
best_model = keras.models.load_model(folder_name)
with open(f"{folder_name}/model_history.txt") as file:
  best_history = json.load(file)

# accuracy plot
plt.plot(best_history['accuracy'])
plt.plot(best_history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# loss plot
plt.plot(best_history['loss'])
plt.plot(best_history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Print the final model values
print("last validation accuracy: ",best_history['val_accuracy'][-1:])
print("last validation loss: ",best_history['val_loss'][-1:], "\n")

best_model.summary()