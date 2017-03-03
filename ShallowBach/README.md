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
3, 180, Note_on_c,  3, 72, 64
[Track Number, timestamp, command, instrument number, pitch, volume]
```

Currently, I process these into the following format:

```
[0, 1, 0], 0.00, 0, 1
[0, 1, 0], 0.25, 0, 0
[0, 0, 1], 0.00, 5, 1
[One-hot track number, normalized delta time, relative pitch, boolean on/off]
```

Relativizing the pitch is an approximate way to transpose pieces in different keys to be the same. However, this technically doesn't achieve that if a piece doesn't begin on the tonic. ([reddit](https://www.reddit.com/r/musictheory/comments/2pv3a7/why_arent_everyone_starting_songs_with_tonics/): "If you want to be a basic bitch you start with the tonic") 
I scraped [this site](http://www.bachcentral.com/midiindexcomplete.html) for Bach midis, and for now only processed the ones with 4 instrument tracks (64 files). I used a NN with 100-node LSTM and 2 more hidden layers of 100-nodes each.

As a proof of concept, I trained this model for just one epoch. The good news is that its output is well-formatted (Bach joke: well-tempered) in that it can sucessfully be converted back into a midi file. It even seems to have somewhat complex rhythm and chords, which I think is very promising! It's odd to me that the chords are perfect fourths, which were considered dissonant in the time of Bach. At any rate, it is a far cry from a fugue. More like a cell phone ringtone... **There is a long way to go.**

*Listen [here](https://soundcloud.com/user-758753778/1epoch)!* Converted to standard notation, this is what the model produced:

![My image](https://github.com/anbrjohn/Misc/blob/master/ShallowBach/1epoch.png)

###Thoughts:

Maybe training this model longer will give better results, but I think there are other things I should tackle first:
- More data. Don't limit myself to just songs with 4 tracks.
- My gut tells me I should format the data differently:
- Tracks: Instead of passing one track at a time with the track number encoded each time, I think it makes more sence to pass all tracks at once (with null values if a track isn't playing anything at that point). I haven't done this yet because it would require bit more coding in the processing module.
- Pitch: Instead of returning a float for the pitch, I think it might be better to encode the notes as a one-hot vector. Then instead of just taking the output, equivalent to the argmax, I could sample from the probability ditribution for more variety. However, that adds a lot of nodes. Perhaps I could encode delta pitch for different timesteps...
- Duration: If I made the above changes, I think it would be more tractable to go back to a timestep-based setup as opposed to delta time, though this 
- To do so, I would need to rework how I model duration. If only one track is playing at a certain timestamp, I would feed null values for the other ones. I'm unsure whether this would help or hurt performance.
- Idea:

```
120:
67
0

180:
0
72
[Timestamp (for example, not actually fed into model) / Track 1 / Track 2]
```
