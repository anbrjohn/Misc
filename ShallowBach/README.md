###Goal:

Automatically generate music in the style of J.S. Bach. Specifically, train a neural network on midi files of Bach works.

Inspiration Taken from the DeepBach Project:
- https://www.youtube.com/watch?v=QiBM7-5hA6o
- https://arxiv.org/pdf/1612.01010.pdf

###Status:

Very much a work-in-progress. Lots of Frankencode. Beware!

###Structure of midi files:

Instead of directly encoding an audio signal, midi files act as an electronic musical score, with information on volume, pitch, and timing for different tracks. I use this [delightful program](http://www.fourmilab.ch/webtools/midicsv/) to easily convert midi files into human-readable csv files. 

eg: `$ midicsv chorale.mid > chorale.csv`

The meat of the file consists of lines like this:

```
2, 120, Note_on_c,  0, 67, 64
2, 180, Note_off_c, 0, 67, 44
2, 180, Note_on_c,  1, 72, 64
[Track Number, timestamp, command, instrument number, pitch, volume]
```

Currently, I process these into the following format:

```
[0, 1, 0], 0.00, 0, 1
[0, 1, 0], 0.25, 0, 0
[0, 1, 0], 0.00, 5, 1
[One-hot track number, normalized delta time, relative pitch, boolean on/off]
```

I scraped [this site](http://www.bachcentral.com/midiindexcomplete.html) for Bach midis, and for now only processed the ones with 4 instrument tracks (64 files). I used a NN with 100-node LSTM and 2 more hidden layers of 100-nodes each.

As a proof of concept, I trained this model for just one epoch. The good news is that its output is well-formatted (Bach joke: well-tempered) in that it can sucessfully be converted back into a midi file. It even seems to have somewhat complex rhythm and chords (perfect fourths), which I think is very promising! Still, it is a far cry from a fugue. More like a cell phone ringtone... **There is a long way to go.**

*Listen [here](https://soundcloud.com/user-758753778/1epoch)!* Converted to standard notation, this is what the model produced:

![My image](https://github.com/anbrjohn/Misc/blob/master/ShallowBach/1epoch.png)

###Thoughts:

Maybe training this model longer will give better results, but I think there are other things I should tackle first:
- More data. Don't limit myself to just songs with 4 tracks.
- More/different pre-processing. Is this the best way to organize the data to train the network? I don't mean anything computationally expensive, just something I need to think out a bit more and put into code.
- Instead of returning a float for the pitch, I think it might be better to encode the notes as a one-hot vector. Then instead of just taking the output, equivalent to the argmax, I could sample from the probability ditribution for more variety. However, that adds a lot of nodes. Perhaps I could encode delta pitch for different timesteps...
- Conversely, I am not convinced that I like my current one-hot track encoding system. It seems more intuitive to me to feed the pitch and volume (0 or 1) for each voice into the system simulateously.
- To do so, I would need to rework how I model duration. If only one track is playing at a certain timestamp, I would feed null values for the other ones. I'm unsure whether this would help or hurt performance.
