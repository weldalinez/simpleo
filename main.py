# import processes as coba #untuk versi diconvert ke romaji
import processesjp as coba #untuk versi tidak diconvert ke romaji
import time

startTime = time.time()
n = 2
w = 2
p = 2
student = 1
question = 5
human_rater = [35, 73, 36, 62, 42, 75, 90, 65, 86, 68, 97, 57, 15, 77, 92, 97, 93, 96, 80, 87, 88, 98, 94, 96, 98, 79,
               79, 81, 70, 74, 37, 81, 37, 77, 90, 73, 42, 96, 87, 94, 88, 63, 72]

list_score = []

# jumlah mahasiswa
for count in range(1, student + 1):
    print('===========================================================================================================')
    print("MAHASISWA", count, "\n")
    # jumlah soal
    arr_score = []
    current_score = 0
    score = 0
    doc = coba.read_txt("mahasiswa" + str(count) + ".docx")
    # print(doc)
    for q in range(0, question):
        kj = 1
        scores = []
        scores1 = []
        print('\n\nJAWABAN ', q + 1)

        # process the student's answer document
        prep = coba.preprocessing(doc[q])                       #delete repetitive from question, convert to romaji(if needed), filter text
        ngramprep = coba.nGram(prep)                            #ngram process
        # sdict = coba.dictionary(ngramprep)                   #create dictionary from students' answers

        #print all processes' results
        # print('---\npreprocessing siswa\n', prep)
        # print('---\nngram siswa\n', ngramprep)
        # print('---\ndict siswa\n', sdict, '\n')
        # pemrosesan untuk tiap kunci

        key = coba.read_txt("jwbDosen" + str(q + 1) + ".docx")  #read answer key documents
        #for each answer keys (from each questions)
        for x in range(0, len(key)):
            print('----------------')
            print('KUNCI JAWABAN '+str(kj))

            #process answer keys
            prep2 = coba.preprocessing(key[x])                  #delete repetitive from question, convert to romaji(if needed), filter text
            ngramprep2 = coba.nGram(prep2)                      #ngram process
            kjdict = coba.dictionary(ngramprep2)               #create dictionary from students' answers
            kjtrans = coba.transform(ngramprep2)
            strans = coba.transform(ngramprep)
            # kjdict = coba.dictionary(prep2)  # create dictionary from students' answers
            # kjtrans = coba.transform(prep2)
            # strans = coba.transform(prep)
            scoring = coba.frobeniusNorm(kjtrans,strans)
            scoring1 = coba.scoring2(kjtrans,strans)
            scores.append(scoring)
            scores1.append(scoring1)

            #print all processes' results
            # print('---\npreprocessing dosen\n', prep2)
            # print('---\npreprocessing siswa\n', prep)
            # print('---\nngram dosen\n', ngramprep2)
            print('---\nngram siswa\n', ngramprep)
            print('---\ndict dosen\n', kjdict)
            print('---\nvector kunci jawaban\n', kjtrans)
            print('---\nvector siswa\n', strans)
            # print('---\n(FN) Nilai KJ ke-', kj, '\t: ', scoring)
            # print('---\n(JC) Nilai KJ ke-', kj, '\t: ', scoring1, '\n---\n')

            kj += 1 #loop for each answer keys
        print('\n\n(JC) Nilai Soal Nomor', q + 1, '\t: ', max(scores1))
        print('(FN) Nilai Soal Nomor', q + 1,'\t: ', max(scores), '\n--------------------------')
        arr_score.append(max(scores))
    print('\n\nNILAI MAHASISWA ', count, '\t: ', round(sum(arr_score),2))
    list_score.append(round(sum(arr_score),2))
print("===========================================================================================================\nNilai-nilai siswa: ", list_score)
print("Program Execution Duration: ", (time.time() - startTime), "seconds")