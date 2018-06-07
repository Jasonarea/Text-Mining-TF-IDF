import os
import operator
from math import log10
from math import sqrt
import codecs

allFreq = {}
testAllFreq = {}
wordList = []
testWordList = []
tfDic = {}
testTfDic = {}
pickWord = []
freq = {}
testFreq = {}


def getTestNNPNNG(line):
    split = line.split('\t')
    if len(split) > 1:
        if split[-1].__contains__("NNP") or split[-1].__contains__("NNG"):
            # print(split[-1])
            find = split[-1].split("+")
            for i in range(0, len(find)):
                if find[i].__contains__("NNP") or find[i].__contains__("NNG"):
                    findStr = find[i][:find[i].find('/')]
                    if findStr.__contains__("’"):
                        findStr = findStr[:findStr.find('’')]

                    if findStr.__contains__("”"):
                        if findStr.find("”") == 0:
                            findStr = findStr[findStr.find('”'):]
                        else:
                            findStr = findStr[:findStr.find('”')]

                    co = testFreq.get(findStr, 0)
                    if not findStr in testWordList:
                        testWordList.append(findStr)
                    else:
                        testFreq[findStr] = co + 1
                        # print(findStr)
                    count = frequency.get(findStr, 0)
                    frequency[findStr] = count + 1


def getNNPNNG(line):
    split = line.split('\t')
    if len(split) > 1:
        if split[-1].__contains__("NNP") or split[-1].__contains__("NNG"):
            # print(split[-1])
            find = split[-1].split("+")
            for i in range(0, len(find)):
                if find[i].__contains__("NNP") or find[i].__contains__("NNG"):
                    findStr = find[i][:find[i].find('/')]
                    if findStr.__contains__("’"):
                        findStr = findStr[:findStr.find('’')]

                    if findStr.__contains__("”"):
                        if findStr.find("”") == 0:
                            findStr = findStr[findStr.find('”'):]
                        else:
                            findStr = findStr[:findStr.find('”')]

                    co = freq.get(findStr, 0)
                    if not findStr in wordList:
                        wordList.append(findStr)
                    else:
                        freq[findStr] = co + 1
                        # print(findStr)
                    count = frequency.get(findStr, 0)
                    frequency[findStr] = count + 1


fileCo = 0
testFileCo = 0
wordCo = 0
testWordCo = 0
wordDic = {}
testWordDic = {}
realFreq = {}
testRealFreq = {}
freqIndex = 0
testFreqIndex = 0

# Calculate TF in Input_Data
for root, dirs, files in os.walk('C:/Users/hyeon/Desktop/가천대학교 데이터마이닝 프로젝트(180524)/Corpus/Input_Data'):
    for fname in files:
        full_name = os.path.join(root, fname)
        if full_name.__contains__("DS"): continue
        # print(full_name)
        file = codecs.open(full_name, 'r', "utf-8")
        lines = file.readlines()
        total_str = ""
        frequency = {}
        for line in lines:
            getNNPNNG(line)  # frequency setting 까지 완료

        allFreq[fileCo] = list(frequency.keys())  # 파일당  word list를 allFreq에 저장
        # freq[fileCo] = frequency
        fileCo += 1

        for words in frequency:
            frequency[words] = log10(frequency[words] + 1)  # TF : frequency dictionary

        tfDic[fileCo] = frequency

# Calculate TF in TestData
for root, dirs, files in os.walk('C:/Users/hyeon/Desktop/가천대학교 데이터마이닝 프로젝트(180524)/Corpus/Test_Data'):
    for fname in files:
        full_name = os.path.join(root, fname)
        if full_name.__contains__("DS"): continue
        # print(full_name)
        file = codecs.open(full_name, 'r', "utf-8")
        lines = file.readlines()
        total_str = ""
        frequency = {}
        for line in lines:
            getTestNNPNNG(line)  # frequency setting 까지 완료

        testAllFreq[testFileCo] = list(frequency.keys())  # 파일당  word list를 allFreq에 저장
        # freq[fileCo] = frequency
        testFileCo += 1

        for words in frequency:
            frequency[words] = log10(frequency[words] + 1)  # TF : frequency dictionary

        testTfDic[testFileCo] = frequency

sortedArr = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
print(sortedArr)
sortFreq = []
i = 0
for word in sortedArr:
    if i >= 5000: break
    sortFreq.append(sortedArr[i][0])
    i += 1

# Calculate IDF
# wordFreqFile 은 파일마다의 키리스트 (이중리스트)
i = 0
for word in wordList:
    wordFreqFile = allFreq.values()
    # print(i)
    i += 1
    for wordFile in wordFreqFile:
        if word in wordFile:
            wordCo = wordDic.get(word, 0)
            wordDic[word] = wordCo + 1

wordDic.items()

for words in wordDic:
    wordDic[words] = log10(len(wordFreqFile) / wordDic[words])  # IDF : wordDic dictionary

# Calculate testdata IDF
# wordFreqFile 은 파일마다의 키리스트 (이중리스트)
i = 0
for word in testWordList:
    wordFreqFile = testAllFreq.values()
    # print(i)
    i += 1
    for wordFile in wordFreqFile:
        if word in wordFile:
            wordCo = testWordDic.get(word, 0)
            testWordDic[word] = wordCo + 1

for words in testWordDic:
    testWordDic[words] = log10(len(wordFreqFile) / testWordDic[words])  # IDF : testWordDic dictionary

# Input_data의 TF_IDF 구하기
sortDic = {}
for p_id, p_info in tfDic.items():
    print("ID : ", p_id)
    for key in p_info:
        for word in wordDic:
            if key == word:
                p_info[key] = wordDic[word] * p_info[key]  # Calculate TF-IDF
        for word in sortFreq:
            if key == word:
                sortDic[word] = p_info[key]  # 각각의 5000개의 word와 TF-IDF mapping


# Test_data의 TF_IDF 구하기
testSortDic = {}
for p_id, p_info in testTfDic.items():
    print("ID : ", p_id)
    for key in p_info:
        for word in testWordDic:
            if key == word:
                p_info[key] = testWordDic[word] * p_info[key]  # Calculate TF-IDF
        for word in sortFreq:
            if key == word:
                testSortDic[word] = p_info[key]  # 각각의 5000개의 word와 TF-IDF mapping

# allFreq를 사용하여 파일당 wordList에서 5000개의 단어에 포함된 단어만 찾기
# sortDic 의 key는 5000개의 단어, value는 각 단어에 대한 TF-IDF
newFileDic = []
for fileId, fileWord in allFreq.items():
    newDic = []
    for word in sortDic.keys():
        if word in fileWord :
            newDic.append(sortDic[word])
        else:
            newDic.append(0)
    newFileDic.append(newDic)
    # print(newDic)

# Test data의 값에 5000개의 TF_IDF mapping
testNewFileDic = []
for fileId, fileWord in testAllFreq.items():
    newDic = []
    for word in sortDic.keys():
        if word in testSortDic.keys():
            newDic.append(testSortDic[word])
        else:
            newDic.append(0)
    testNewFileDic.append(newDic)
    # print(newDic)

# Normalization
sum = [0 for i in range(fileCo)]
j = 0
for files in newFileDic:
    for i in files:
        if i != 0:
            sum[j] += (i * i)
    sum[j] = sqrt(sum[j])
    print("Sum : ", sum[j])
    j += 1

for i in range(0, fileCo):
    for j in range(0, len(newFileDic[i])):
        if newFileDic[i][j] != 0:
            newFileDic[i][j] = newFileDic[i][j] / sum[i]
        print(newFileDic[i][j])

# TestData normalization
testSum = [0 for i in range(testFileCo)]
j = 0
for files in testNewFileDic:
    for i in files:
        if i != 0:
            testSum[j] += (i * i)
    testSum[j] = sqrt(testSum[j])
    j += 1

for i in range(0, testFileCo):
    for j in range(0, len(testNewFileDic[i])):
        if testNewFileDic[i][j] != 0:
            testNewFileDic[i][j] = testNewFileDic[i][j] / testSum[i]
        print(testNewFileDic[i][j])

# write the Normalized TF-IDF value in txt file
directory = os.listdir("C:/Users/hyeon/Desktop/201236552_정현선/Input_Data")
fileNum = [128, 219, 166, 120, 191, 112, 172, 252, 327]
print(directory)
fileDirectory = {}
fileCount = 0
for file in directory:
    fileDirectory[file] = fileNum[fileCount]
    fileCount += 1

fileCount = 0
for file_id, fileInfo in fileDirectory.items():
    for i in range(0, fileDirectory[file_id]):
        fileName = "C:/Users/hyeon/Desktop/201236552_정현선/Input_Data/" + file_id + "/" + "(POS)" + file_id + "_" + str(
            i + 1) + ".txt"
        fw = open(fileName, 'w')
        for j in range(0, len(newFileDic[i])):
            fw.write(str(newFileDic[i][j]) + "\t")

# Write Test-Data
directory = os.listdir("C:/Users/hyeon/Desktop/201236552_정현선/Test_Data")
testFileNum = [10, 10, 10, 10, 10, 10, 10, 10, 10]
print(directory)
testFileDirectory = {}
fileCount = 0
for file in directory:
    testFileDirectory[file] = testFileNum[fileCount]
    fileCount += 1
fileCount = 0
for file_id, fileInfo in testFileDirectory.items():
    for i in range(0, testFileDirectory[file_id]):
        fileName = "C:/Users/hyeon/Desktop/201236552_정현선/Test_Data/" + file_id + "/" + "(POS)" + file_id + "_" + str(fileDirectory[file_id] + i + 1) + ".txt"
        fw = open(fileName, 'w')
        for j in range(0, len(testNewFileDic[i])):
            fw.write(str(testNewFileDic[i][j]) + "\t")
