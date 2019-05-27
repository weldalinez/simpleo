from pykakasi import kakasi  # untuk proses mengubah karakter jp ke roman
import re  # regular expression
import docx2txt
import tinysegmenter
from math import *

kakasi = kakasi()
particles = ['te','masu','wa','ka','ga','ni','no','e','o','wo','to','ya','nado','mo','de','kara','yori','made','kurai','hodo','bakari','toiu','toka','demo','tokoro','node','nara','ba','temo','sae','noni','nagara','tari','desu','desuka','shi','tomo','yara','dano','kurai','dake','nari','koso','tewa','toshite','nomi','yo','kana','na','naa','sa','koto','mono','ze','zo','yara','tara']

# read documents, .txt or .docx
def read_txt(doc):
    read1 = docx2txt.process(doc)
    read = read1.splitlines()  # split document to lists on new line
    read = [x for x in read if not x.isdigit()]  # remove number from words
    read = [x for x in read if x]  # remove empty list
    return read

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
    text = ' '.join(tinysegmenter.tokenize(text_jpn))
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


# n gram
def nGram(text):
    global tokens
    tokens = [text for text in text.split(" ") if text != ""]
    print('---\nTokens\n', tokens)
    global ngramres
    ngramres=[]
    for n in range(1,len(tokens)):
        for num in range(len(tokens)):
            ngram = ' '.join(tokens[num:num + n])
            if len(ngram.split()) == n:
                ngramres.append(ngram)
    i = 0
    while i < len(ngramres):
        if ngramres[i] in particles:
            del ngramres[i]
        else:
            i += 1
    return ngramres


# run preprocessing
def preprocessing(text):
    text = remove_rep(text)
    romaji = to_romaji(text)
    # print(romaji)
    filtering = filter_text(romaji)
    return filtering


def dictionary(sentence):
    """Magic n-gram function fits to vector indices."""
    global indices
    indices = {}
    i, inp = len(indices) - 1, sentence
    for n in range(len(tokens)):
        for x in zip(*[inp[n:]]):
            if indices.get(x) == None:
                i += 1
                indices.update({x: i})
    return indices

def transform(sentence):
    """Given a sentence, convert to a gram vector."""
    v, inp = [0] * len(indices), sentence
    for n in range(len(tokens)):
        for x in zip(*[inp[i:] for i in range(n)]):
            if indices.get(x) != None:
                v[indices[x]] += 1
    return v

#cosine
def scoring1(text1, text2):
    # scores = []
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(text1)):
            x = text1[i]
            y = text2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
            if sumyy == 0:
                score = 0
            else:
                score = sumxy / math.sqrt(sumxx * sumyy)
            # scores.append(score)
    return score

#jaccard similarity
def scoring2(x,y):
    similar = []
    for n in range(len(x)):
        if y[n] == x[n]:
            similar.append(y[n])
    jaccard = (len(similar)/len(x))*20
    # print('---\nsimilar :', similar)
    return jaccard

#Euclidean distance
def scoring3(x,y):
    similar = []
    for n in range(len(x)):
        if y[n] == x[n]:
            similar.append(y[n])
    # jaccard = (len(similar)/len(x))*20
    # print('---\nsimilar :', similar)
    return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

#frobenius norm
def frobeniusNorm(x,y):
    similar = []
    for n in range(len(x)):
        if y[n] == x[n]:
            similar.append(y[n])
    # print('---\nsimilar :', similar)
    fnormRef = sqrt(sum(i * i for i in x))     # find frobenius norm of human rater's answer key
    fnormTest = sqrt(sum(i * i for i in similar))   # find frobenius norm of student's answer
    fnorm = (fnormTest / fnormRef) * 20                 # calculate score from fnorm
    fnorm = round(fnorm, 2)                             # round to 2 decimal points
    if fnorm > 20:                                      # if score > 20, change it to 20
        fnorm = 20
    return fnorm