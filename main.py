import processes as coba

n = 2
w = 2
p = 2
student = 1
question = 5
human_rater = [35, 73, 36, 62, 42, 75, 90, 65, 86, 68, 97, 57, 15, 77, 92, 97, 93, 96, 80, 87, 88, 98, 94, 96, 98, 79,
               79, 81, 70, 74, 37, 81, 37, 77, 90, 73, 42, 96, 87, 94, 88, 63, 72]

# jumlah mahasiswa
for count in range(1, student + 1):
    print('===========================================================================================================')
    print("MAHASISWA", count)
    # jumlah soal
    arr_score = []
    temp_score = []
    doc = coba.read_txt("mahasiswa" + str(count) + ".docx")
    print(doc)
    for q in range(0, question):
        # process the student's answer document
        print('-------------------------------------------------------')
        print('Jawaban', q+1)
        prep = coba.preprocessing(doc[q])
        ngramprep = coba.nGram(prep)
        print(prep)
        print(ngramprep, '\n')
        current_score = 0
        score = 0
        key = coba.read_txt("jwbDosen"+str(q+1)+".docx")
        # pemrosesan untuk tiap kunci
        kj=1
        for x in range(0, len(key)):
            print('Kunci Jawaban '+str(kj))
            # key = coba.read_txt("key" + str(q) + "-" + str(x) + ".docx")
            prep2 = coba.preprocessing(key[x])
            print('prep2')
            print(prep2)
            ngramprep2 = coba.nGram(prep2)
            print('ngramprep2')
            print(ngramprep2)
            kj+=1
#---------------------------------------------------------------------------------------------------------------------------------------------
#comment dulu
            # winnowing = coba.winnow(prep, p, n, w)
            # winnowing2 = coba.winnow(prep2, p, n, w)
            # # similarity measurement
            # jac_measure = coba.jaccard(winnowing, winnowing2)
            # dice_measure = coba.dice(winnowing, winnowing2)
            # cos_measure = coba.cosine(winnowing, winnowing2)
            # # print("jaccard : " + str(jac_measure) + " | dice : " + str(dice_measure) + " | cosine : " + str(cos_measure))
            # # nilai terbesar dari ketiga metode pengukuran
# ---------------------------------------------------------------------------------------------------------------------------------------------
# comment dulu
#             score = max(jac_measure, dice_measure, cos_measure)
#             temp_score = score
#             if current_score <= temp_score:
#                 current_score = temp_score
#             else:
#                 continue
#---------------------------------------------------------------------------------------------------------------------------------------------
#dicomment dulu
    #     print("\nNilai Nomor " + str(q+1) + " : " + str(current_score))
    #     # print(current_score)
    #     arr_score.append(current_score)
    # print('-------------------------------------------------------')
    # # nilai total
    # average = sum(arr_score) / len(arr_score)
    # print("Total Skor     : " + str(average))
    # # print(average)
    # # akurasi sistem
    # acc = 100 - (((abs(average - human_rater[count - 1])) / 100) * 100)
    # print("Human Rater    : " + str(human_rater[count - 1]))
    # # print(human_rater[count-1])
    # print("Akurasi Sistem : " + str(acc))
    # # print(acc)