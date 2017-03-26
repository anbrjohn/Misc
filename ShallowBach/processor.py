
import numpy as np


gran = 32 # Granularity (smallest note duration captured)
    
def do_format(text):
    formatted = []
    for line in text:
        line = line.split(", ")
        line[1] = int(line[1])
        if line[2].lower() == "note_on_c" or line[2].lower() == "note_off_c":
            formatted += [line]
    formatted = sorted(formatted, key=lambda i:i[1])
    return formatted


#Makes note values relative to the first one
def transpose(data, offset=40):
    start = int(data[0][4]) - offset # Zero reserved for silence
    for line in data:
        line[4] = str(int(line[4]) - start)  
    return data


#Changes timestamp to relative durations
def timing(data, metronome, granularity=gran): #Formatted text and smallest note represented (eg. 32nd)
    last = 0
    for line in data:
        last = str(line[1])
        line[1] = line[1] / metronome #Normalized (1.0 = one quarter note)
        line[1] = round(line[1] * (np.log2(granularity) - 1), 0)
    return data


#Further organizes format, sets note_off command to pitch value of 0
def trim(data):
    output = []
    for line in data:
        voice = int(line[0])
        timing = int(line[1])
        note = int(line[4])
        on_off = line[2]
        if on_off.lower() == "note_on_c":
            note = int(line[4])
        else: #Note_off_c
            note = 0
        output.append([timing, voice, note])
    output.sort()
    return output


def expand(data, number_of_voices):
    voices = number_of_voices - 1
    start = data[0][0]
    stop = data[-1][0] 
    data = data[::-1] # Reverse it for popping
    # Initialize array: Incremental timesteps x voices
    timesteps = np.zeros(((stop - start), voices))
    all_voices = np.zeros(voices)
    time, voice, pitch = data.pop()
    for i in range(start, stop):
        while time == i:
            all_voices[voice - 2] = pitch
            try:
                time, voice, pitch = data.pop()
            except: # If no data left to pop
                time = "skip" # To break out of while loop
        timesteps[i - start] = all_voices
        # Buffer at end to help signal end of song
    buffer = np.zeros((10, voices))
    timesteps = np.vstack((timesteps, buffer))
    return timesteps


def encode(filename):    
    with open(filename) as f:
        text = f.readlines()
    header = text[0].split(", ")
    number_of_voices = int(header[4])
    metronome = int(header[5])
    f1 = do_format(text)
    f2 = transpose(f1, offset=50)
    f3 = timing(f2, metronome)
    f4 = trim(f3)
    f5 = expand(f4, number_of_voices)
    return f5

f = encode(filename)


# Removes repeat information for timesteps
def collapse(data):
    data = data.T
    change_log = []
    voice_num = 2
    for voice in data:
        i = 0
        # Find first note for a track that is not 0
        while voice[i] == 0 and i < len(voice) - 1: 
            i += 1
        change_log.append((i, voice_num, voice[i])) #Timestep, voice, and note
        for time in range(i, len(voice)):
            note = round(voice[time])
            # If current note is different than the last one
            if note != change_log[-1][2]: 
                change_log.append((time, voice_num, note))
        voice_num += 1
    return change_log

    
# Redoes some formatting and adds in note_off commands at pitch transitions
def un_organize(data, metronome=480, granularity=gran):
    time_factor = metronome / (np.log2(granularity) - 2)
    new = []
    prev_voice = 0
    for time, voice, note in data:
        time = time * time_factor
        if note != 0:
            command = 'Note_on_c'
            volume = 70
        else:
            # Would be a problem if 1st note of a voice is 0
            command = 'Note_off_c' 
            volume = 0
        # Add note_off command for previous pitch at current timestep
        if prev_voice != voice: # If this is the first note of a new track
            prev_voice = voice
            prev_note = note
        else:
            off_line = [voice, int(time), 'Note_off_c', 0, int(prev_note), 0]
            new.append(off_line)
            
        line = [voice, int(time), command, 0, int(note), volume]
        new.append(line)
        prev_note = note
    return new
    
    
def undo_format(data, metronome=480):
    number_of_voices = data[-1][0]
    last_timestep = max([x[1] for x in data]) + 2
    line1 = "0, 0, Header, 1, "+str(number_of_voices)+", "+str(metronome)+"\n"
    line2 = "1, 0, Start_track\n"
    line3 = "1, " + str(last_timestep+5) + ", End_track\n"
    line4 = "2, 0, Start_track\n"
    formatted = [line1, line2, line3, line4]
    data = sorted(data)
    last = 2
    indecies = []
    for i in range(len(data)):
        voice = data[i][0]
        if voice != last:
            indecies += [i-3]
            last = voice
    for line in data:
        line[0] = str(line[0]) # Voice
        line[1] = str(line[1]) # Time
        line[3] = str(line[3]) # Instrument
        line[4] = str(line[4]) # Note
        line[5] = str(line[5]) # Volume
        line = ", ".join(line)
        formatted += [line + "\n"]
    # Add markers for start/stop of tracks
    voice = 2
    for point in indecies:
        end = str(voice) + ", " + str(last_timestep) + ", End_track\n"
        voice += 1
        start = str(voice) + ", 0, Start_track\n"
        insert_point = point + (voice * 2) + 1
        formatted.insert(insert_point, end)
        formatted.insert(insert_point+1, start)
    end = str(voice) + ", " + str(last_timestep) + ", End_track\n"
    formatted.append(end)
    formatted.append("0, 0, End_of_file\n")
    return formatted


def decode(data):
    u3 = collapse(data)
    u2 = un_organize(u3)
    u1 = undo_format(u2)    
    return u1

#To later convert into midi
def make_csv(filename, data): 
    with open(filename, "w") as f:
        for line in data:
            f.write(line)
    print("Saved as", filename)
    
u = decode(f)





def encode_multiple(filenames):
    all_data = []
    for file in filenames:
        data = encode(file, info=False)
        for line in data:
            all_data.append(line)
    print("Done")
    return all_data


import os
midis = [file for file in os.listdir() if file[-4:] == ".txt"]

#Go over all midi files in a folder

info = []
for file in midis:
    with open(file) as f:
        try:
            text = f.readlines()
            line = text[0]
            line = line.split(", ")
            tempo = int(line[-1])
            voices = int(line[-2])
        except:
            print(file)
    info.append([voices, tempo, file])
 
#Find files that have only 4 voices
voices = 4
file_info = [x for x in info if x[0] <= (voices+1)]
files = [x[-1] for x in file_info]
len(files)



# Process all of those files together
def process_all(target_voice_number):
    file_info = [x for x in info if x[0] <= (target_voice_number+1)]
    files = [x[-1] for x in file_info]
    print(len(files), "files found")  
    # Process all files
    all_data = []
    for file in files:
        data = encode(file)
        # Add empty lines for any unused voices
        while data.shape[1] < target_voice_number:
            empty_voice = np.zeros([len(data),1])
            data = np.hstack([data,empty_voice])
        for line in data:
            all_data.append(line)
    print("Done")
    return all_data

all_data = process_all(4)


def save_data(filename, data): #For training NN
    with open(filename, "w") as f:
        for line in data:
            string = str(line)[1:-1]+"\n"
            f.write(string)
    print("Done")
    
    
def read_data(filename):
    new_data = []
    for line in data:
        new_line = line.split(", ")
        newer_line = []
        for item in new_line:
            if len(item) > 0:
                item = int(item)
            newer_line.append(item)
        new_data.append(newer_line)
    return new_data
