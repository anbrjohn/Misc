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


def get_xy(data, seqlen=3, y_type="float"):
    """Prepare data. y_type can be float, 1-hot, or 4-hot"""
    voices = 4
    dataX = [] # Represenation of consecutive notes (of length seqlen)
    dataY = [] # Representation of the following notes
    length = len(data[0]) # Number of features for each element
    for i in range(len(data) - seqlen):
        x_data = np.array(data[i:i+seqlen])
        x_data = x_data.flatten()
        dataX.append(x_data)
        dataY.append(data[i+seqlen])
    x = np.reshape(dataX, (len(dataX), seqlen*length, 1))
    x = x/100 #NN prefers floats
    dataY[-1] = dataY[-2][:] #Last element was empty and had wrong length
    y = np.array(dataY)
    
    y_type = str(y_type)[0].lower()
    if y_type == "f":
        y /= 100
    elif y_type == "1":
        notes = int(max(np.array(data).flatten())) + 1
        print("Notes:", notes) # Length of 1-hot vector for each voice
        size = len(x)
        all_lines = np.zeros([size, notes * voices])
        for timestep in range(size):
            # A 1-hot vector for each voice, concatenated together
            concat_lines = np.array([])
            for voice in y[timestep]:
                line = np.zeros([notes])
                line[int(voice)] = 1
                concat_lines = np.hstack([concat_lines, line])
            all_lines[timestep] = concat_lines
        y = all_lines
    elif y_type == "4":
        y = to_categorical(y) #Convert to "four-hot" encoding
    return x, y


x, y = get_xy(all_data, seqlen=3, y_type=4)

model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(x.shape[1], x.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(100, activation="relu"))
model.add(Dense(y.shape[1], activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

model.fit(x,y, batch_size=32, nb_epoch=1, verbose=1)

#For 1-hot
def get_notes(prediction, considered_notes=4):
    note_values = []
    for i in range(considered_notes):
        note = np.argmax(prediction)
        # Append pitch and probability
        note_values.append((note, prediction[note]))
        # Turn off so next-highest will now be returned
        prediction[note] = 0
    return note_values


def guess_note(prediction):
    note_values = []
    noteprobs = get_notes(prediction)
    prob_sum = sum([n[1] for n in noteprobs])
    probs = [n[1]/prob_sum for n in noteprobs] # Normalize probabilities
    notes = [n[0] for n in noteprobs]
    guess = np.random.choice(notes, 1, p=probs)
    guess = guess.tolist()
    return guess[0]


def consec3(seed, iterations):
    voices = 4
    s = seed * 100
    s = s.T.tolist()[0]
    # Only works if seqlen=3 !!
    total = [s[:voices], s[voices:voices * 2], s[voices * 2:voices * 3]]
    next_seed = seed
    for i in range(iterations):
        prediction = model.predict(np.array([next_seed]))
        notes = int(len(prediction[0]) / voices)
        new_line = np.zeros(voices)
        for voice in range(voices):
            voice_prediction = prediction[0][notes*voice:notes*(voice+1)]
            guess = guess_note(voice_prediction)
            new_line[voice] = guess
        total.append(new_line.tolist())        
        next_seed = next_seed[voices:].tolist()
        for guess in new_line.tolist():
            next_seed.append([guess/100])
        next_seed = np.array(next_seed)
    return np.array(total)

def compose3(seed, iterations, save=False):
    total = consec3(seed, iterations)
    final = decode(total)
    if save:
        make_csv(str(save), final)
    print("Done")
    


def final_transpose(text, offset):
    formatted = []
    for line in text:
        line = line.split(", ")
        if line[2].lower() == "note_on_c" or line[2].lower() == "note_off_c":
            line[4] = str(int(line[4]) + offset)       
            formatted += [line]
        else:
            formatted += [line]
    transposed = []
    for line in formatted:
        line = ", ".join(line)
        transposed.append(line)
    return transposed


#To later convert into midi
def make_csv2(filename, data): 
    with open(filename, "w") as f:
        for line in data:
            f.write(line)
    print("Saved as", filename)
    
def adjust(filename, pitch, speed, output_title):
    with open(filename) as f:
        text = f.readlines()
    header = text[0].split()
    header[5] = str(speed) + "\n"
    header = " ".join(header)
    text[0] = header
    adjusted = final_transpose(text, pitch)
    make_csv2(output_title, adjusted)
    
#adjust(filename, 30, 120, "4H10e.csv")

seed = s2
filename = "60e3.csv"
compose3(seed, 240, save=filename)
adjust(filename, 15, 240 , filename)
