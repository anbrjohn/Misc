import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.core import Dropout
from keras.layers.recurrent import LSTM
from keras.utils.np_utils import to_categorical
from keras.callbacks import History 
from keras.models import model_from_json
import pylab
import random


def get_xy(data, seqlen=4):
    """Prepare data"""
    dataX = [] # Represenation of consecutive notes (of length seqlen)
    dataY = [] # Representation of the following notes
    length = len(data[0]) # Number of features for each element
    for i in range(len(data) - seqlen):
        x_data = np.array(data[i:i+seqlen])
        x_data = x_data.flatten()
        dataX.append(x_data)
        dataY.append(data[i+seqlen])
    x = np.reshape(dataX, (len(dataX), seqlen*length, 1))
    dataY[-1] = dataY[-2][:] #Last element was empty and had wrong length
    y = np.array(dataY)
    return x, y

x,y = get_xy(all_data2)


model = Sequential()
model.add(LSTM(100, input_shape=(x.shape[1], x.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(100, activation="relu"))
model.add(Dense(100, activation="relu"))
model.add(Dense(y.shape[1], activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

model.fit(x,y, batch_size=16, nb_epoch=1, verbose=1)

def more_process(prediction):
    lis = prediction.tolist()
    for entry in lis:
        entry[0] *= 480 # Duration
        entry[1] *= 89 # Note pitch
        entry[0] = round(entry[0], 5)
        entry[1] = round(entry[1], 5)
        entry[2] = round(entry[2]) # Boolean on/off
        one_hot = max(entry[-5:])
        for i in range(5):
            if entry[i-5] == one_hot:
                #index = i-5
                entry[i-5] = 1
            else:
                entry[i-5] = 0
    prediction = np.array(lis).flatten()
    prediction = np.array([prediction.tolist()]).T
    return prediction

def consecutive(seed, iterations):
    total = [seed]
    next_seed = seed
    for i in range(iterations):
        prediction = model.predict(next_seed)
        prediction = more_process(prediction)
        next_seed = seed.tolist()
        next_seed = next_seed[1:]+[prediction.tolist()]
        next_seed = np.array(next_seed)
        total.append(next_seed)
    return total

def split(data):
    separated = []
    for entry in data:
        for y in entry:
            separated.append(y[:8])
            separated.append(y[8:16])
            separated.append(y[16:24])
            separated.append(y[24:])
    return separated

def unprocess(prediction):
    new = []
    entry = prediction.flatten().tolist()
    #new.append(int(entry[0] * 480)) # Duration
    new.append(int(entry[0])) # Duration
    pitch = int(entry[1] * 89)
    new.append(pitch)
    new.append(int(entry[2])) #Boolean on/off
    if entry[3] == 1:
        new.append(-1)
    elif entry[4] == 1:
        new.append(2)
    elif entry[5] == 1:
        new.append(3)
    elif entry[6] == 1:
        new.append(4)
    elif entry[7] == 1:
        new.append(5)
    return new

def compose(seed, iterations, save=False):
    total = []
    many = consecutive(seed, iterations)
    for x in split(many):
        unprocessed = unprocess(x)
        if unprocessed[1] < 101:
            total.append(unprocessed)
    final = decode(total, 65, 5)
    if save:
        make_csv(str(save), final)
    print("Done")


seed_start = 0
seed = x[seed_start:seed_start+4]
compose(seed,10,"1epoch.txt")
    
