from pykakasi import kakasi  # untuk proses mengubah karakter jp ke roman
import re  # regular expression
import docx2txt
import tinysegmenter

kakasi = kakasi()


# read documents, .txt or .docx
def read_txt(doc):
    read1 = docx2txt.process(doc)
    read = read1.splitlines()  # split document to lists on new line
    read = [x for x in read if not x.isdigit()]  # remove number from words
    read = [x for x in read if x]  # remove empty list
    return read


'''
mulai  preprocessing
1. menghilangkan kata-kata yang mengulang soal
2. romanisasi, konversi kana ke romaji
3. whitespace removal, menghapus spasi dan enter
4. case folding, menyeragamkan ke lower case
5. filtering, menghapus selain huruf dan angka

'''


# menghapus kata yang mengulang soal
def remove_rep(text):
    rep_words = ["2020年東京オリンピックのマスコットは", "ハラルは", "ハラルというは", "ハラルというのは",
                 "生前退位は", "生前退位というは", "生前退位というのは",
                 "衆院選は", "衆院選というは", "衆院選というのは",
                 "Uターンは", "Uターンのは", "Uターンというは", "Uターンというのは",
                 "Uターン就職は", "Uターン就職というは", "U-ターン就職というのは"]

    word_list = set(rep_words)
    for words in word_list:
        if words in text:
            text = text.replace(words, "")
    return text


# mengubah katakana, hiragana, dan kanji ke romaji (romanisasi)
def to_romaji(text_jpn):
    segmenter = tinysegmenter.TinySegmenter()
    text = ' '.join(segmenter.tokenize(text_jpn))
    kakasi.setMode("H", "a")  # Hiragana ke romaji
    kakasi.setMode("K", "a")  # Katakana ke romaji
    kakasi.setMode("J", "a")  # Japanese ke romaji
    kakasi.setMode("r", "Hepburn")  # default: Hepburn Roman table
    # kakasi.setMode("s", True) # add space, default: no separator
    # kakasi.setMode("C", True) # capitalize, default: no capitalize
    convert = (kakasi.getConverter()).do(text)
    return convert


# filtering
def filter_text(romaji):
    filtering = re.sub("\n", "", romaji).casefold()
    filtering = re.sub("[^A-Za-z0-9]+", " ", filtering)
    return filtering


# selesai preprocessing


'''
mulai winnowing
1. pembentukan ngram (penggalan lata) sebanyak n
2. hashing, konversi tiap karakter pada ngram ke bentuk hash dengan rumus rolling hash
3. windowing, tiap hash yang dibentuk dikelompokkan ke window sepanjang w
4. fingerprinting, memilih fingerprint terkecil dari tiap window, jika ada nilai yang sama yang diambil yang ada di window paling kanan

'''


# n gram
def nGram(text):
    tokens = [text for text in text.split(" ") if text != ""]
    print('tokens')
    print(tokens)
    ngramres=[]
    for n in range(1,len(tokens)):
        for num in range(len(tokens)):
            ngram = ' '.join(tokens[num:num + n])
            if len(ngram.split()) == n:
                ngramres.append(ngram)
    return ngramres


# hashing
def to_hash(text, p):
    result = 0
    length = len(text)
    ascii_code = [ord(i) for i in text]  # mengubah ke ascii
    for i in range(length):
        result = result + (ascii_code[i] * pow(p, length - 1))  # rumus rolling hash
        length = length - 1
    return result


def hashing(ngram, p):
    roll_hash = [to_hash(ngram[i], p) for i in range(len(ngram))]
    return roll_hash


# windowing
def windowing(roll_hash, w):
    window = [roll_hash[i:i + w] for i in range(len(roll_hash) - w + 1)]
    return window


# fingerprint
def fingerprint(window, w):
    fingers = []
    current_min = None
    # untuk tiap window
    for i in range(0, len(window)):
        minimum = window[i][0]
        # untuk window sepanjang w
        for j in range(1, w):
            if window[i][j] <= minimum:
                minimum = window[i][j]
        # menyimpan nilai minimum tiap window ke list
        if current_min != minimum:
            fingers.append(minimum)
        elif minimum == window[i][w - 1]:
            fingers.append(minimum)
        current_min = minimum
    return fingers


# selesai winnowing


'''
mulai similarity measurement, mencari tingkat kesamaan fingerprint
1. jaccard similarity
2. dice coefficient
3. cosine similarity
'''


# jaccard similarity
def jaccard(fingerprint1, fingerprint2):
    num = len(set(fingerprint1).intersection(set(fingerprint2)))
    denum = len(set(fingerprint1).union(set(fingerprint2)))
    if denum == 0:
        jaccard = 0.0
    else:
        jaccard = float(num / denum) * 100
    return jaccard


# dice coefficient
def dice(fingerprint1, fingerprint2):
    num = 2 * (len(set(fingerprint1).intersection(set(fingerprint2))))
    denum = len(set(fingerprint1)) + len(set(fingerprint2))
    if denum == 0:
        dice = 0.0
    else:
        dice = float(num / denum) * 100
    return dice


# cosine similarity
def cosine(fingerprint1, fingerprint2):
    num = len(set(fingerprint1).intersection(set(fingerprint2)))
    denum = (len(set(fingerprint1)) ** .5) * (len(set(fingerprint2)) ** .5)
    if denum == 0:
        cosine = 0.0
    else:
        cosine = float(num / denum) * 100
        if cosine > 100:
            cosine = 100.0
    return cosine


# selesai similarity measurement

# run preprocessing
def preprocessing(text):
    text = remove_rep(text)
    romaji = to_romaji(text)
    # print(romaji)
    filtering = filter_text(romaji)
    return filtering


# run winnowing
def winnow(text, p, n, w):
    ngram = nGram(text, n)
    roll_hash = hashing(ngram, p)
    window = windowing(roll_hash, w)
    fingerprinting = fingerprint(window, w)
    return fingerprinting

#vectorizing
def vectorizing1(text):
    """Magic n-gram function fits to vector indices."""
    indices={}
    i, inp = len(indices) - 1, text.split()
    for n in n_list:
        for x in zip(*[inp[i:] for i in range(n)]):
            if indices.get(x) == None:
                i += 1
                indices.update({x: i})


def transform(self, text):
    """Given a text, convert to a gram vector."""
    n_list = n_list
    indices={}
    v, inp = [0] * len(indices), text.split()
    for n in n_list:
        for x in zip(*[inp[i:] for i in range(n)]):
            if indices.get(x) != None:
                v[indices[x]] += 1
    return v