from pykakasi import kakasi  # untuk proses mengubah karakter jp ke roman
import re  # regular expression
import docx2txt
import tinysegmenter
from math import *
from numpy import zeros, sum            # library to create a matrix, etc.
from scipy.linalg import svd            # library for the svd process

kakasi = kakasi()
# particles = ['ほど','が','か','かしら','かな','かないうちに','がはやいか','から','きり','くらい','けれども','こそ','こと','さ','さえ','し','しか','しかない','すら','ぜ','ぞ','だけ','だけに','だの','たら','たり','で','ては','でも','ても','と','と いう','という','とか','ところ','どころか','ところで','として','とも','ともあろうひと','な','なあ','ながら','など','なら','なり','に','にしては','について','にとって','ね','ねえ','の','ので','のです','のに','のみ','ば','は','ばいい','ばかり','ばかりでなく','ばかりに','へ','ほど','まで','までもない','も','もの','ものか','ものの','や','やいなや','やら','よ','より','わ','を','をする']
particles = ['hodo','ga','ka','kashira','kana','ka nai uchi ni','ga hayai ka','kara','kiri','kurai','keredomo','koso','koto','sa','sae','shi','shika','shika nai','sura','ze','zo','dake','dake ni','dano','tara','tari','de','tewa','demo','temo','to','to iu','toka','tokoro','dokoro ka','tokoro de','toshite','tomo','tomo aroo hito','na','naa','nagara','nado','nara','nari','ni','ni shite wa','ni tsuite','ni totte','ne','nee','no','node','no desu','noni','nomi','ba','wa','ba','bakari','bakari de naku','bakari ni','e','hodo','made','made mo nai','mo','mono','monoka','mono no','ya','ya ina ya','yara','yo','yori','wa','wo','o','wo suru','o suru']

# read documents, .txt or .docx
def read_txt(doc):
    read1 = docx2txt.process(doc)
    read = read1.splitlines()                       # split document to lists on new line
    read = [x for x in read if not x.isdigit()]     # remove number from words
    read = [x for x in read if x]                   # remove empty list
    return read

# Erase the questions' sentences from answers
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

#
def to_romaji(text_jpn):
    text = ' '.join(tinysegmenter.tokenize(text_jpn))
    kakasi.setMode("H","a") # Hiragana ke romaji
    kakasi.setMode("K","a") # Katakana ke romaji
    kakasi.setMode("J","a") # Japanese ke romaji
    kakasi.setMode("r","Hepburn") # default: Hepburn Roman table\
    convert = (kakasi.getConverter()).do(text)
    return convert

# filtering
def filter_text(romaji):
    words = re.sub('[ ・。、\n]+', '', romaji)  # replace "・", "。", "、", " ", and "\n" with ""
    return words

# run preprocessing
def preprocessing(text):
    text = remove_rep(text)
    filtering = filter_text(text)
    romaji = to_romaji(filtering)
    return romaji

# n gram
def nGram(text):
    global tokens
    tokens = tinysegmenter.tokenize(text)
    # print('---\ntokens\n', tokens)
    global ngramres
    ngramres=[]
    for n in range(1,len(tokens)):
        for num in range(len(tokens)):
            ngram = ' '.join(tokens[num:num + n])
            if len(ngram.split()) == n:
                ngram = ngram.replace(" ", "")
                ngramres.append(ngram)

    # For Scenario 1 (N-Gram without Particles)
    # i = 0
    # while i < len(ngramres):
    #     if ngramres[i] in particles:
    #         del ngramres[i]
    #     else:
    #         i += 1

    # For Scenario 2 (N-Gram with Particles Without Frequency of Occurrence)
    # ngramres = list(dict.fromkeys(ngramres))
    return ngramres

def TDMRef(ngramprep2):
    A = zeros([len(ngramprep2), 1])
    for i, k in enumerate(ngramprep2):
        A[i] += 1
    return A

def TDMTest(ngramprep2, ngramprep):
    if len(ngramprep) == 0:
        A = [[0.]]
    else:
        A = zeros([len(ngramprep), 1])
        for k in range(len(ngramprep)):
            if ngramprep[k] in ngramprep2:
                A[k] += 1
            else:
                A[k] = 0
    return A

def SVD(A):
    URef, S, VtRef = svd(A)
    return S

def frobeniusNorm(svdkj, svds):
    fnormRef = sqrt(sum(i * i for i in svdkj))     # find frobenius norm of human rater's answer key
    fnormTest = sqrt(sum(i * i for i in svds))   # find frobenius norm of student's answer
    fnorm = (fnormTest / fnormRef) * 20                 # calculate score from fnorm
    fnorm = round(fnorm, 2)                             # round to 2 decimal points
    if fnorm > 20:                                      # if score > 20, change it to 20
        fnorm = 20
    return fnorm