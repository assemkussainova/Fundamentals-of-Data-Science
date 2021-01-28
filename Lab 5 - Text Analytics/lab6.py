# import necessary libraries
import numpy as np
import random

print("'TEXT ANALYTICS' PROGRAM")


# ask to enter the name of the dataset file and load the raw data in some data structure
file = input("Enter the name of the dataset file: ")
with open(file) as f:
	raw_data = f.read()


# print the number of characters in the file (should be 5101618)
ch_number = len(raw_data)


# split the raw data into sentences and save in some data structure (delimiter for sentence boundaries: '\n')
data = raw_data.split('\n')
data = [sent for sent in data if sent != '']


# print the number of sentences on that file (should be  42068)
sent_number = len(data)


# copy the data into another datastructure and add '<bos>' and '<eos>' symbols to the beginning and ending of each sentence respectively, e.g. "how are you"  => "<bos> how are you <eos>"
data2 = data.copy()
for i in range(len(data2)):
	data2[i] = ''.join(('<bos>', data2[i], '<eos>'))


# print the sentences from each copies to verify that only the second one contains the modifications
check1 = data[0]
check2 = data2[0]


# perform additional preprocessing based on the dataset
words = []
for string in data2:
	s = string.split()
	for e in s:
		words.append(e)

dictionary = dict()
for w in words:
	if w in dictionary:
		dictionary[w] += 1
	else:
		dictionary[w] = 1

sumM = sum(dictionary.values())
dictionary_prob = dict()
for i in dictionary:
	dictionary_prob[i] = dictionary[i]/sumM


# write additional subroutines/local functions needed for the execution of each options
def compute_prob0(sentence, dictionary_prob):
	string = sentence.split()
	prob = 1
	for w in string:
		if w in dictionary_prob:
			prob *= dictionary_prob[w]
		else:
			prob *= dictionary_prob['<unk>']
	return prob


def compute_prob1(se, d, dct):
	se = ''.join(('<bos>', ' ', se, ' ', '<eos>'))
	se = se.split(' ')
	for i in range(len(se)):
		if se[i] not in d:
			se[i] = "<unk>"

	p = 1
	for i in range(len(se) - 1):
		count = 0
		for j in range(len(d) - 1):
			if (se[i] == d[j]) & (se[i + 1] == d[j + 1]):
				count += 1
		if count > 0:
			p *= count / dct[se[i]]
	return p


def compute_prob2(s, d, dct):
	s = ''.join(('<bos>', ' ', s, ' ', '<eos>'))
	s = s.split(' ')
	for i in range(len(s)):
		if s[i] not in d:
			s[i] = "<unk>"

	p = 1
	for i in range(len(s) - 2):
		count = 0
		for j in range(len(d) - 2):
			if (s[i] == d[j]) & (s[i + 1] == d[j + 1]) & (s[i + 2] == d[j + 2]):
				count += 1
		if count > 0:
			p *= count / dct[s[i]]
	return p


def autofill1(n, w, dt):
	nex = dict()
	for i in range(len(dt) - 1):
		if dt[i] == w:
			if dt[i + 1] in nex:
				nex[dt[i + 1]] += 1
			else:
				nex[dt[i + 1]] = 1

	sortedAns = sorted(nex, key=nex.get, reverse=True)

	if len(sortedAns) >= int(n):
		return sortedAns[0:int(n)]
	else:
		return "Try another number"


def autofill2(n, w1, w2, dt):
	nex = dict()
	for i in range(len(dt) - 2):
		if (dt[i] == w1) & (dt[i + 1] == w2):
			if dt[i + 2] in nex:
				nex[dt[i + 2]] += 1
			else:
				nex[dt[i + 2]] = 1

	sortedAns = sorted(nex, key=nex.get, reverse=True)

	if len(sortedAns) >= int(n):
		return sortedAns[0:int(n)]
	else:
		return "Try another number"


def generate_text0(n, dat):
	for i in range(int(n)):
		choose = np.random.choice(dat)
		if choose != '<bos>' and choose != '<eos>':
			first_word = choose
		sentence = [first_word]
		n_words = random.randint(1, 7)

		for i in range(n_words):
			w = np.random.choice(dat)
			if w != '<bos>' and w != '<eos>':
				sentence.append(w)
		sentence = ' '.join(sentence)
		print(' '.join(('<bos>', sentence, '<eos>')))


def generate_text1(n, dat):
	def create_dict(a):
		for i in range(len(a) - 1):
			yield (a[i], a[i + 1])

	chain_dict = create_dict(dat)

	word_dict = {}
	for present, future in chain_dict:
		if present in word_dict.keys():
			word_dict[present].append(future)
		else:
			word_dict[present] = [future]

	for i in range(int(n)):
		choose = np.random.choice(dat)
		if choose != '<bos>' and choose != '<eos>':
			first_word = choose
		sentence = [first_word]
		n_words = random.randint(1, 7)

		for i in range(n_words):
			w = np.random.choice(word_dict[sentence[-1]])
			if w != '<bos>' and w != '<eos>':
				sentence.append(w)
		sentence = ' '.join(sentence)
		print(' '.join(('<bos>', sentence, '<eos>')))


def generate_text2(n, dat):
	def create_dict(d):
		for i in range(len(d) - 2):
			yield (d[i], d[i + 1], d[i + 2])

	chain_dict = create_dict(dat)

	word_dict = {}

	for present, present2, future in chain_dict:
		dkey = [present, present2]
		if tuple(dkey) in word_dict.keys():
			word_dict[tuple(dkey)].append(future)
		else:
			word_dict[tuple(dkey)] = [future]

	for i in range(int(n)):
		first_word = []
		index = random.randint(0, len(dat) - 1)
		key = (dat[index], dat[index + 1])
		if '<bos>' not in key and '<eos>' not in key:
			first_word = key
		sentence = list(first_word)
		n_words = random.randint(1, 7)

		for i in range(n_words):
			w = np.random.choice(word_dict[key])
			if w != '<bos>' and w != '<eos>':
				sentence.append(w)
			key = (key[1], w)
		output = ' '.join(sentence)
		print(' '.join(('<bos>', output, '<eos>')))


# the sceleton of the menu-driven program
finished = False

print("Number of characters in the file: ", ch_number)
print("Number of sentences in the file: ", sent_number)
print("Check values for modification: \n", check1, "\n", check2, "\n")

while not finished:
	print("------------------------------------------")
	print("Available options (enter corresponding number to choose): \n")
	print("1. Estimate probability of sentence.")
	print("2. Autocomplete phrase.")
	print("3. Generate new text.")
	print("4. Exit. \n")
	option = input("Enter number of option: ")
	option = int(option)

	if option == 1:

		order = input("Choose an order of Markov chain (0, 1, 2): ")
		sentence = input("Enter your sentence: \n")

		if order == "0":
			pr = compute_prob0(sentence, dictionary_prob)
			print("The probability of your sentence is ", pr)
		elif order == "1":
			pr = compute_prob1(sentence, words, dictionary)
			print("The probability of your sentence is ", pr)
		elif order == "2":
			pr = compute_prob2(sentence, words, dictionary)
			print("The probability of your sentence is ", pr)

	elif option == 2:

		order = input("Choose an order of Markov chain (1, 2): ")
		k = int(input("Number of words to autocomplete: "))

		if order == "1":
			word = input("Enter your word: \n")
			auto = autofill1(k, word, words)
			print("Your predicted words are: ", auto)
		elif order == "2":
			word = input("Enter your first word: ")
			word2 = input("Enter your second word: \n")
			auto = autofill2(k, word, word2, words)
			print("Your predicted words are: ", auto)

	elif option == 3:

		order = input("Choose an order of Markov chain (0, 1, 2): ")
		k = int(input("Number of sentences to generate: \n"))

		if order == "0":
			if k <= 1:
				print("Your sentence is: ")
				gen = generate_text0(k, words)
			else:
				print("Your sentences are: ")
				gen = generate_text0(k, words)
		elif order == "1":
			if k <= 1:
				print("Your sentence is: ")
				gen = generate_text1(k, words)
			else:
				print("Your sentences are: ")
				gen = generate_text1(k, words)
		elif order == "2":
			if k <= 1:
				print("Your sentence is: ")
				gen = generate_text2(k, words)
			else:
				print("Your sentences are: ")
				gen = generate_text2(k, words)

	elif option == 4:
		print("Quitting....")
		finished = True
