# -*- coding: utf-8 -*-

#Andrew Johnson, 2015
#anbrjohn@indiana.edu

#for Python 2.7.9
#nltk required to run

"""Scans a text to find 'poetry possibilities.'

That is, for all permutations of words in text {T},
this returns all words {W:W⊂U)}  that rhyme with word {R:R⊂T}
while also being synonymous with another word {S:S⊂T},
output in the format (R, S, [W1, W2, ... Wn]).

For words with multiple possible POS (eg: "record"),
applies the NLTK tagger and searches only for words with the same POS.
For words with multiple possible pronunciations, searches through all pronunciations. eg:
route + sturdy = stout
route + shrewd = astute
"""

from __future__ import division
import nltk
from collections import defaultdict
import re #regular expressions

#synonym corpus
from nltk.corpus import wordnet as wn

#pronunciation corpus
entries = nltk.corpus.cmudict.entries()

#turn pronunciation corpus into a dictionary
#dictionary["route"] --> [[u'R', u'UW1', u'T'], [u'R', u'AW1', u'T']]
dictionary = defaultdict(list)
for x in entries:
    dictionary[x[0]].append(x[1])

###

def basic_rime(pronunciation):
    """returns the rime of the final syllable of a *single* pronunciation as a list
    basic_rime([u'P', u'AY1', u'TH', u'AA0', u'N']) --> u'AAN' """
    destressed = [phoneme.strip(r"[012]") for phoneme in pronunciation] #removes stress
    pronunciation = "".join(destressed) #combines phonomes into one string
    final_vowel = re.findall(r'[AEIOU]+', pronunciation)[-1] #determines final vowel in word
    location = pronunciation.rindex(final_vowel) #determines location of final vowel
    basic_rime = pronunciation[location:]
    return basic_rime

def rime(word):
    """returns the rime of all pronunciations as a string
    rime("route") --> [[u'UWT'], [u'AWT']]"""
    rimes = []
    if word.lower() in dictionary:
        word = dictionary[word.lower()]
        rimes += [[basic_rime(pronunciation)] for pronunciation in word]
    return rimes

###

def tag(sent):
    """tags POS
    tag("Did you record that record?") -->
    [('Did', 'NNP'), ('you', 'PRP'), ('record', 'VB'), ('that', 'DT'), ('record', 'NN'), ('?', '.')]
    However, tagger tends to tag initial adjectives as nouns for some reason."""
    sent = nltk.word_tokenize(sent)
    sent_tagged = nltk.pos_tag(sent)
    return sent_tagged

def check_pos(tagged_word):
    """checks if POS is noun, verb, adj, or adverb, and changes nltk tag to match wordnet one
    check(('talked', 'VBD')) --> 'v'"""
    pos = tagged_word[1][0]
    if pos == "N":
        return "n"
    elif pos == "V":
        return "v"
    elif pos == "R":
        return "r"
    elif pos == "J":
        return "a"

def tagged_thesaurus(tagged_word):
    """"returns synonyms of a word of the same POS
    th("slow", "v") --> [u'decelerate', u'slow', u'slow_down', ... ]
    th("slow", "a") --> [u'slow', u'dense', u'dim', u'dull', ...]"""
    synonym_list = []
    word = tagged_word[0].lower()
    pos = check_pos(tagged_word)
    for meaning in wn.synsets(word):
        syn_pos = str(meaning)[-6]
        if syn_pos == "s":
            syn_pos = "a"
        if pos == syn_pos:
            synonym_set = meaning.lemma_names()
            [synonym_list.append(syn) for syn in synonym_set if syn not in synonym_list]
            #also evalutes nouns as adjectives because nltk tagger has a bad habit of mis-tagging
        elif pos == "n" and syn_pos == "a":
            synonym_set = meaning.lemma_names()
            [synonym_list.append(syn) for syn in synonym_set if syn not in synonym_list]
    return synonym_list

###

def check_rhyme(word1, word2):
    """checks if two words rhyme (including potential multiple pronunciations)
    check_rhyme("route", "about") --> True
    check_rhyme("route", "astute") --> True"""
    word1 = rime(word1)
    word2 = rime(word2)
    for pronunciation in word1:
        if pronunciation in word2:
            return True

def tagged_rhyme_and_relate(rhyme, tagged_relate):
    """finds words that rhyme with word A and are also synonymous with word B
    rnr(("route", "NN"), "sturdy") --> [u'stout']"""
    synonyms = tagged_thesaurus(tagged_relate)
    return [word for word in synonyms if
            check_rhyme(rhyme.lower(), word) and word.lower() != rhyme and word.lower() !=tagged_relate[0]]

###

def find(rhyme, text):
    text = tag(text)
    words = []
    for tagged_word in text:
        one_set = tagged_rhyme_and_relate(rhyme, tagged_word)
        if len(one_set) > 0:
            words += [(rhyme, tagged_word[0], one_set)]
    return words

def full_find(text):
    split_text = re.split(" ", text) #splits into words.
    split_text = [word.strip(r"!?\"\',.") for word in split_text] #removes basic punctuation
    all_words = [] 
    for rhyme in split_text:
        all_words += find(rhyme, text)
    return all_words

def suggestions(text):
    all_words = full_find(text)
    for entry in all_words:
        print "Try replacing '%s' with %s, which rhymes with '%s'." % (entry[1], entry[2], entry[0])
