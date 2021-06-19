# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pickle

import numpy
import numpy as np
from tqdm import tqdm


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def epigenemi(fileName):
    with open(f'data/{fileName}') as file:
        lines = [line.rstrip() for line in file]
        numberOfTests = int(lines[0])
        i = 1
        iterator = 0
        while iterator < numberOfTests:
            # print(i, '|', lines[i])
            numberOfCases, lengthOfCases = tuple(int(x) for x in lines[i].split(' '))
            seq = []
            # print(lines[i])

            for j in range(i + 1, i + numberOfCases + 1):
                # print(lines[j])
                # print(numberOfCases, lengthOfCases, numberOfTests)
                seq.append(list(lines[j]))
            # print(numpy.transpose(seq))
            rawdata = list(map(lambda x: ''.join(x), numpy.transpose(seq)))
            coll = {v: k for k, v in enumerate(list(dict.fromkeys(rawdata).keys()))}

            lengthOfColl = len(coll)
            indexses = ''
            # print(rawdata)
            # print(coll)
            for c in rawdata:
                # print(c)
                indexses += f'{coll[c] + 1} '
            print(lengthOfColl)
            print(indexses)
            i = i + numberOfCases + 1
            iterator += 1


def metabolite(fileName):
    out = ''
    fN = f'data2/{fileName}'
    # lines = [line.rstrip() for line in file]
    # numberOfTests = int(lines[0])
    import linecache
    numberOfTests = int(linecache.getline(fN, 1))
    i = 2
    iterator = 0
    while iterator < numberOfTests:
        # print(i, '|', lines[i])

        numberOfCases = 3
        # firstRow, secondRow, thirdRow = tuple(int(x) for x in lines[i].split(' '))
        seq = []
        massExcludedList = None
        seqs = None
        flattenList = None
        # print(lines[i])

        for j in range(i + 1, i + numberOfCases + 1):
            # print(lines[j])
            # seq.append(list(map(lambda x: float(x), lines[j].split(' '))))
            seq.append(np.fromstring(linecache.getline(fN, j), dtype=np.float64, sep=' '))
        print("Data Reading Progress Finished")
        i = i + numberOfCases + 1
        iterator += 1
        # print(len(seq), len(seq[0]))
        filteredList = np.array([seq[1] + x for x in seq[0]], dtype=np.float64)
        seqs = seq[2]
        del seq
        # filteredList = np.where(temp > 0, temp, float('inf'))
        shp = filteredList.shape
        flattenList = filteredList.flatten()
        del filteredList

        # with open('flattedList.pickle', 'wb') as handle:
        #     pickle.dump(flattedList, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # return
        # enumeratedList = {k: v for k, v in enumerate(flattenList)}
        # del flattenList
        # sortedList = dict(sorted(enumeratedList.items(), key=lambda item: item[1]))
        # del enumeratedList
        # keys = np.fromiter(sortedList.keys(), dtype=int)
        # vals = np.fromiter(sortedList.values(), dtype=float)
        # vals = np.abs(vals)

        # del sortedList
        # massExcludedList
        print("Aggregation Progress Finished")

        for mof in tqdm(seqs):  # masses of signal
            massExcludedList= None
            massExcludedList = np.abs(flattenList - mof)

            # key = keys[np.argmax(vals >= mof)
            # key = np.argwhere(massExcludedList ==np.min(massExcludedList))
            # reduced = vals[key:key+10000]
            # key = keys[np.argmax(reduced >= mof)]
            indexes = np.unravel_index(massExcludedList.argmin(), shp)
            # print(key, mof)
            out += f"{' '.join(str(v + 1) for v in indexes)}\n"
            # for k, v in sortedList.items():
            #     if v >= mof:
            #         # out += f"{k / r} {k % c}\n"
            #         indexes = np.unravel_index(k,shp)
            #         out += f"{' '.join(str(v + 1) for v in indexes)}\n"
            #         # print(indexes)
            #
            #         break
            # indexes = np.argwhere(massExcludedList == np.min(massExcludedList))[0] + 1
            # indexes = np.unravel_index(massExcludedList.argmin(), massExcludedList.shape)
            # indexes = np.unravel_index(massExcludedList.argmin(), massExcludedList.shape)
            # out += f"{' '.join(str(v + 1) for v in indexes)}\n"
        # print(values)
        # print(temp - mof, mof)
    print("Result Checking Progress Finished")

    f = open(f'res2/res{fileName}', 'w')
    f.write(out)  # python will convert \n to os.linesep
    f.close()  #


def metabolite2(fileName):
    out = ''
    with open(f'data2/{fileName}') as file:
        lines = [line.rstrip() for line in file]
        numberOfTests = int(lines[0])
        i = 1
        iterator = 0
        while iterator < numberOfTests:
            # print(i, '|', lines[i])
            numberOfCases = 3
            # firstRow, secondRow, thirdRow = tuple(int(x) for x in lines[i].split(' '))
            seq = []
            # print(lines[i])
            for j in range(i + 1, i + numberOfCases + 1):
                # print(lines[j])
                # seq.append(list(map(lambda x: float(x), lines[j].split(' '))))
                seq.append(np.fromstring(lines[j], dtype=np.float64, sep=' '))

            i = i + numberOfCases + 1
            iterator += 1
            print("Data Reading Progress Finished")

            filteredList = np.array([seq[1] + x for x in seq[0]], dtype=np.float64)
            # filteredList = np.where(filteredList > 0, filteredList, float('inf'))
            # filteredList[filteredList < 0] = np.inf
            print("Aggregation Progress Finished")
            ind = 0

            for mof in tqdm(seq[2]):  # masses of signal

                minimum = float('inf')
                for index, x in np.ndenumerate(filteredList):
                    massExcludedList = np.abs(x - mof)
                    if minimum > massExcludedList:
                        minimum = massExcludedList
                        indexes = index
                    # indexes = np.argwhere(massExcludedList == np.min(massExcludedList))[0] + 1
                # indexes = np.unravel_index(minimum, filteredList.shape)
                out += f"{indexes[0] + 1}{indexes[1] + 1}\n"
                print(ind, indexes[0] + 1, indexes[1] + 1, minimum)

                ind += 1
                # print(values)
                # print(temp - mof, mof)

    print("Result Checking Progress Finished")
    f = open(f'res2/res{fileName}', 'w')
    f.write(out)  # python will convert \n to os.linesep
    f.close()  #


def metabolite3(fileName):
    out = ''
    with open(f'data2/{fileName}') as file:
        lines = [line.rstrip() for line in file]
        numberOfTests = int(lines[0])
        i = 1
        iterator = 0
        while iterator < numberOfTests:
            # print(i, '|', lines[i])
            numberOfCases = 3
            # firstRow, secondRow, thirdRow = tuple(int(x) for x in lines[i].split(' '))
            seq = []
            # print(lines[i])
            for j in range(i + 1, i + numberOfCases + 1):
                # print(lines[j])
                # seq.append(list(map(lambda x: float(x), lines[j].split(' '))))
                seq.append(np.fromstring(lines[j], dtype=np.float64, sep=' '))

            i = i + numberOfCases + 1
            iterator += 1
            print("Data Reading Progress Finished")

            filteredList = np.array([seq[1] + x for x in seq[0]], dtype=np.float64)
            # filteredList = np.where(filteredList > 0, filteredList, float('inf'))
            # filteredList[filteredList < 0] = np.inf
            print("Aggregation Progress Finished")
            ind = 0

            for mof in tqdm(seq[2]):  # masses of signal
                massExcludedList = np.abs(filteredList - mof)

                indexes = np.argwhere(massExcludedList == np.min(massExcludedList))[0] + 1
                # indexes = np.unravel_index(awr, filteredList.shape)
                out += f"{indexes[0] + 1}{indexes[1] + 1}\n"
                # print(ind, indexes[0] + 1, indexes[1] + 1, indexes)

                ind += 1
                # print(values)
                # print(temp - mof, mof)

    print("Result Checking Progress Finished")
    f = open(f'res2/res{fileName}', 'w')
    f.write(out)  # python will convert \n to os.linesep
    f.close()  #


def metabolite4(fileName):
    out = ''
    with open(f'data2/{fileName}') as file:
        lines = [line.rstrip() for line in file]
        numberOfTests = int(lines[0])
        i = 1
        iterator = 0
        while iterator < numberOfTests:
            # print(i, '|', lines[i])
            numberOfCases = 3
            # firstRow, secondRow, thirdRow = tuple(int(x) for x in lines[i].split(' '))
            seq = []
            # print(lines[i])
            for j in range(i + 1, i + numberOfCases + 1):
                # print(lines[j])
                # seq.append(list(map(lambda x: float(x), lines[j].split(' '))))
                seq.append(np.fromstring(lines[j], dtype=np.float64, sep=' '))

            i = i + numberOfCases + 1
            iterator += 1
            print("Data Reading Progress Finished")

            afreq = (np.max(seq[0]) - np.min(seq[0])) * len(seq[0])
            mfreq = (np.max(seq[1]) - np.min(seq[1])) * len(seq[1])
            aList = dict(sorted(enumerate(seq[0]), key=lambda item: item[1]))
            mList = dict(sorted(enumerate(seq[1]), key=lambda item: item[1]))
            print(afreq, mfreq)
            for inn in seq[2]:
                m = inn * mfreq
                valM = aList[int(m)]
                a = (valM - inn) * afreq
                valA = mList[int(a)]
                print(inn, inn - (valM + valA), int(a), int(m))
                out += f"{int(a) + 1}{int(m) + 1}\n"
            print("Result Checking Progress Finished")
            f = open(f'res2/res{fileName}', 'w')
            f.write(out)  # python will convert \n to os.linesep
            f.close()  #


def readFromPickle():
    with open('flattedList.pickle', 'rb') as handle:
        b = pickle.load(handle)
    enumeratedList = {k: v for k, v in enumerate(b)}

    with open('sortedList.pickle', 'wb') as handle:
        pickle.dump(enumeratedList, handle, protocol=pickle.HIGHEST_PROTOCOL)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import time

    start = time.time()
    # for i in range(1, 2):
    metabolite('4.txt')
    # readFromPickle()
    end = time.time()
    print((end - start))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
