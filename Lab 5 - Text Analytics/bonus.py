import syllables

print("Textual Analysis - Readability program")

file_name = input("Enter the name of the dataset file: ")


# Conduct some pre-processing of the selected text, to remove all of the word delimiters other than spaces or the
# end-of-sentence period.
def preprocess_data(file):
    with open(file) as f:
        raw_data = f.read()

    data = raw_data.split('\n')
    data = [sent for sent in data if sent != '']

    data2 = data.copy()
    for i in range(len(data2)):
        data2[i] = ''.join(('<bos>', data2[i], '<eos>'))
    return data2


# Count the total words, total sentences, and total syllables.
def calculate_totals(d, sent, word):
    for s in d:
        sent.append(s)
        sentence = s.split()
        for w in sentence:
            if w != '<bos>' and w != '<eos>':
                word.append(w)

    syl_num = 0
    for w in word:
        syl = syllables.estimate(w)
        syl_num += syl

    sent_num = len(sent)
    word_num = len(word)

    return sent_num, word_num, syl_num


# Count complex words (syllables >= 3, no verbs, no names, no compound words)
def c_words(w, c):
    for word in w:
        syl = syllables.estimate(word)
        if ("-" not in word) and (word.islower() == True) and (syl >= 3) and (word.endswith('es') == False) and (
                word.endswith('ed') == False) and (word.endswith('ing') == False):
            c.append(word)

    cwords_num = len(c)
    return cwords_num


# Calculate Flesch Reading Ease measure
def f_readingease(s, w, sy):
    return 206.835 - 1.015 * (w / s) - 84.6 * (sy / w)


# Calculate Flesch-Kincade Grade Level
def f_gradelevel(s, w, sy):
    return 0.39 * (w / s) + 11.8 * (sy / w) - 15.59


# Calculate Gunning Fog Index
def g_fogindex(s, w, comp):
    return 0.4 * ((w / s) + 100 * (comp / w))


# Calculate SMOG Index
def smog_index(s, n):
    g1 = s[0:10]
    g2 = s[10:20]
    g3 = s[20:30]

    s1 = []
    w1 = []
    cg1 = []
    sent1, word1, syl1 = calculate_totals(g1, s1, w1)

    s2 = []
    w2 = []
    cg2 = []
    sent2, word2, syl2 = calculate_totals(g2, s2, w2)

    s3 = []
    w3 = []
    cg3 = []
    sent3, word3, syl3 = calculate_totals(g3, s3, w3)

    c1 = c_words(w1, cg1)
    c2 = c_words(w2, cg2)
    c3 = c_words(w3, cg3)

    c_num = c1 + c2 + c3
    return 1.0430 * ((c_num * 30 / n) ** (1 / 2)) + 3.1291


# the sceleton of the menu-driven program
finished = False


while not finished:
    print("------------------------------------------")
    print("Available options (enter corresponding number to choose): \n")
    print("1. Flesch Reading Ease measure")
    print("2. Flesch-Kincade Grade Level")
    print("3. Gunning Fog Index")
    print("4. SMOG Index")
    print("5. Exit. \n")

    option = input("Enter number of option: ")
    option = int(option)

    dat = preprocess_data(file_name)

    sentences = []
    words = []
    complex_words = []

    sent, word, syl = calculate_totals(dat, sentences, words)
    comp = c_words(words, complex_words)

    if option == 1:

        print("Ease measure: ", f_readingease(sent, word, syl))

    elif option == 2:

        print("Grade level: ", f_gradelevel(sent, word, syl))

    elif option == 3:

        print("Grade level: ", g_fogindex(sent, word, comp))

    elif option == 4:

        print("Grade level: ", smog_index(sentences, sent))

    elif option == 5:
        print("Quitting....")
        finished = True
