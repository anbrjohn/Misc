#Steps to encode midi-csv format into one for NN
def do_format(text):
    formatted = []
    for line in text:
        line = line.split(", ")
        line[1] = int(line[1])
        if line[2].lower() == "note_on_c" or line[2].lower() == "note_off_c":
            formatted += [line]
    formatted = sorted(formatted, key=lambda i:i[1])
    return formatted


#Changes timestamp to relative durations
def duration(text): #Formatted text
    last = 0
    for line in text:
        diff = line[1] - int(last)
        last = str(line[1])
        line[1] = diff
    return text


#Makes note values relative to the first one
def rel_note(text, start):###=start_note):
    for line in text:
        line[4] = str(int(line[4]) - start)
    return text
            

#Puts it in the desired format
def organize(text, metronome):
    output = []
    for line in text:
        voice = int(line[0])
        duration = line[1] / metronome
        note = int(line[4])
        on_off = line[2]
        if on_off.lower() == "note_on_c":
            #volume = int(line[5])
            volume = 1 #Boolean volume system
        else: #Note_off_c
            volume = 0
        output.append([duration, note, volume, voice])
    end_marker = [0,0,0,-1] #Necessary?
    output.append(end_marker)
    return output


#Same as above steps but in reverse
#To convert output of NN into midicsv format
def un_organize(text, metronome=480):
    new = []
    for line in text:
        duration = round(line[0] * metronome)
        note = line[1]
        volume = line[2]
        voice = line[3]
        if volume > 0:
            new.append([voice, duration, "Note_on_c", "0", note, str(70)+"\n"]) #Boolean volume system
        else:
            new.append([voice, duration, "Note_off_c", "0", note, str(volume)+"\n"])
    return new[:-1] #Remove end_marker (which was added for training purposes)


def un_note(text, start):
    for line in text:
        line[4] += start
    return text


def un_duration(text):
    total = 0
    for line in text:
        line[1] += total
        total = line[1]
    return text


def undo_format(text, number_of_voices, last_timestamp, metronome=480):
    line1 = "0, 0, Header, 1, "+str(number_of_voices)+", "+str(metronome)+"\n"
    line2 = "1, 0, Start_track\n"
    line3 = "1, " + str(last_timestamp+5) + ", End_track\n"
    line4 = "2, 0, Start_track\n"
    formatted = [line1, line2, line3, line4]
    text = sorted(text)
    
    last = 2
    indecies = []
    for i in range(len(text)):
        voice = text[i][0]
        if voice != last:
            indecies += [i-3]
            last = voice

    for line in text:
        line[0] = str(line[0])
        line[1] = str(line[1])
        line[4] = str(line[4])
        line = ", ".join(line)
        formatted += [line]
    
    # Add markers for start/stop of tracks
    voice = 2
    for point in indecies:
        end = str(voice) + ", " + str(last_timestamp+5) + ", End_track\n"
        voice += 1
        start = str(voice) + ", 0, Start_track\n"
        insert_point = point + (voice * 2) + 1
        formatted.insert(insert_point, end)
        formatted.insert(insert_point+1, start)
    end = str(voice) + ", " + str(last_timestamp+5) + ", End_track\n"
    formatted.append(end)
    formatted.append("0, 0, End_of_file\n")
    
    return formatted


#Putting all of the above together:
def encode(filename, info=True):
    with open(filename) as f:
        text = f.readlines()
    header = text[0].split(", ")
    number_of_voices = int(header[4])
    metronome = int(header[5])
    
    f1 = do_format(text)
    f2 = duration(f1)
    start_note = int(f2[0][4])
    if info:
        print("Number of voices", number_of_voices)
        print("Start note:", start_note)
    f3 = rel_note(f2, start_note)
    f4 = organize(f3, metronome)
    return f4

def decode(data, start_note, number_of_voices):
    u4 = un_organize(data)
    u3 = un_note(u4, start_note) #need to know start_note
    u2 = un_duration(u3)
    last_timestamp = u2[-1][1]
    u1 = undo_format(u2, number_of_voices, last_timestamp)
    return u1

def make_csv(filename, data): #Save the file
    with open(filename, "w") as f:
        for line in data:
            f.write(line)
    print("Saved as", filename)



def encode_multiple(filenames):
    all_data = []
    for file in filenames:
        data = encode(file, info=False)
        for line in data:
            all_data.append(line)
    print("Done")
    return all_data


def process(data, info=True, voice_num=4):
    #durations = len(set([x[0] for x in all_data]))
    notes = len(set([x[1] for x in all_data]))
    for line in data:
        #line[0] /= durations
        line[1] /= notes
        voice = str(line[3])
        if voice == -1: #End of song case
            voice = 1 #Other voices begin with 2. Makes them consecutive.
        for i in range(voice_num):
            line.append(0)
        line[3] = 0
        line[2+int(voice)] = 1
    if info:
        #print("Duration normalizer:", durations)
        print("Notes normalizer:", notes)
    return data
all_data = encode_multiple(filenames)
all_data = process(all_data)


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
