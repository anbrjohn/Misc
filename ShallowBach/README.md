Inspiration Taken from the DeepBach Project:

https://www.youtube.com/watch?v=QiBM7-5hA6o

https://arxiv.org/pdf/1612.01010.pdf

###Goal:

Automatically generate music in the style of J.S. Bach. Specifically, train a neural network on midi files of Bach works.

###Status:

Very much in-the-works. Lots of Frankencode. Beware!

###Structure of midi files:

I use this [delightful program](http://www.fourmilab.ch/webtools/midicsv/) to easily convert midi files into readable csv files. 

eg: `$ csvmidi chorale.mid > chorale.csv`

The meat of the file consists of lines like this:

```
2, 120, Note_on_c, 0, 67, 64
2, 180, Note_off_c, 0, 67, 44
2, 180, Note_on_c, 0, 72, 64
[Track Number, timestamp, command, instrument Number, pitch, volume]
```

Currently, I process these into the following format:

```
[0, 1, 0], 0, 0, 1
[0, 1, 0], 0.25, 0, 0
[0, 1, 0], 0, 5, 1
[One-hot track number, normalized delta time, relative pitch, boolean on/off]
```

I scraped [this site](http://www.bachcentral.com/midiindexcomplete.html) for Bach midis, and for now only processed the ones with 4 instrument tracks.

I used a NN with 100-node LSTM and 2 more hidden layers of 100-nodes each.

After just one epoch of training, the good news, is that its output is well-formatted (Bach joke: well-tempered) in that it can sucessfully be converted back into a midi file. It even seems to have some rhythm and chords! Still, it closer to a cell phone ringtone than a fugue.

###Thoughts:

Maybe training this model longer will give better results, but I think there are other things I should tackle first:
- More data. Don't limit myself to just songs with 4 tracks.
- More/different pre-processing. Is this the best way to organize the data to train the network? I don't mean anything computationally expensive, just something I need to think out a bit more and put into code.
