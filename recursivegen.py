import sys
import random
import urllib
import json
import time

x = 0
the_bible = {}	#key: number of sounds in the word, value is a list of word bibles
word_bible = {}	# key: wordname, value: list of sounds in the word

wordnik_key = sys.argv[1]

for line in open('cmu_rhymedict.txt'):
	words = line.split() #break the line apart into sections, store it in a dictionary of how many syllables it has + a set of the words
	count = len(words) - 1
	word = {words[0]: words[1:]}  #probably too complicated, could just use the word itself

	# if there's already a spot for count in the bible, add it, otherwise create it
	if count in the_bible:
		the_bible[count].append(word)  #a set that contains word
	else:
		the_bible[count] = [word]  #this is a set, not just the word itself, so we can add more words later

	word_bible[words[0]] = words[1:]


def similar_syl(word):
	#take the given word and return a word with the same number of sounds
	given_word = word.upper()
	try:
		word_bible[given_word]
		syl_count = len(word_bible[given_word])
		if syl_count > 0:
			new_word = random.choice(the_bible[syl_count]).keys()[0]
			return new_word
		else:
			return "fail"
	except KeyError:
		return

def same_syls(word_a, word_b):
	word_a = word_a.upper()
	word_b = word_b.upper()
	syl_count_a = len(word_bible[given_word])
	syl_count_b = len(word_bible[given_word])
	if syl_count_a == syl_count_b:
		return True
	else:
		return False

#these functions use the Wordnik API
def rhyming_word(apikey, word):
	resp = urllib.urlopen(
			'http://api.wordnik.com/v4/word.json/' + word + '/relatedWords?' + \
			urllib.urlencode({'api_key': api_key, 'relationshipTypes': 'rhyme'}))
	related_data = json.loads(resp.read())
	if len(related_data) == 0:
		return []
	else:
		return related_data[0]['words']

def get_examples(api_key, word):
	resp = urllib.urlopen(
			'http://api.wordnik.com/v4/word.json/' + word + '/examples?' + \
			urllib.urlencode({'api_key': api_key}))
	examples_data = json.loads(resp.read())
	try:
		examples = [item['text'] for item in examples_data['examples']]
		return examples
	except:
		return


#recursive!
def redo_line(api_key, line):
	words = line.split()
	w = words.pop()
	y = similar_syl(w)
	time.sleep(.2)
	if len(words) > 3:
		new_line = str(' '.join(words))
		try:
			print ' '.join(new_line.split()[-3:]) + " " +y.lower()
		except:
			print ' '.join(new_line.split()[-2:])
		redo_line(api_key, new_line)

for l in sys.stdin:
	new_line = ""
	palabras = l.split()
	for p in palabras:
		try:
			examples = get_examples(wordnik_key, similar_syl(p))
			example = random.choice(examples)
			words_in_example = example.split()
			example = []
			for w in words_in_example:
				if w == p:
					w = similar_syl(p)
					example.append(w.lower())
				else:
					example.append(w)
			example = " ".join(example)
			print example
			redo_line(wordnik_key, example)	#this is recursive!
		except:
			x = 0
		time.sleep(.01)
