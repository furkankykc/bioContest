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
        # print(lines[i])

        for j in range(i + 1, i + numberOfCases + 1):
            # print(lines[j])
            # seq.append(list(map(lambda x: float(x), lines[j].split(' '))))
            seq.append(np.fromstring(linecache.getline(fN, j), dtype=float, sep=' '))
        print("Data Reading Progress Finished")
        i = i + numberOfCases + 1
        iterator += 1
        # print(len(seq), len(seq[0]))
        filteredList = np.array([seq[1] + x for x in seq[0]], dtype=np.float32)

        # filteredList = np.where(temp > 0, temp, float('inf'))
        shp = filteredList.shape
        flattedList = np.matrix.flatten(filteredList)
        del filteredList

        # with open('flattedList.pickle', 'wb') as handle:
        #     pickle.dump(flattedList, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # return
        enumeratedList = {k: v for k, v in enumerate(flattedList)}
        del flattedList
        sortedList = dict(sorted(enumeratedList.items(), key=lambda item: item[1]))
        del enumeratedList
        keys = np.fromiter(sortedList.keys(), dtype=int)
        vals = np.fromiter(sortedList.values(), dtype=float)
        del sortedList
        # massExcludedList
        print("Aggregation Progress Finished")

        for mof in tqdm(np.nditer(seq[2])):  # masses of signal
            # massExcludedList = np.abs(filteredList - mof)

            key = keys[np.argmax(vals >= mof)]
            indexes = np.unravel_index(key, shp)
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
            firstRow, secondRow, thirdRow = tuple(int(x) for x in lines[i].split(' '))
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
            filteredList[filteredList < 0] = np.inf
            print("Aggregation Progress Finished")

            for mof in tqdm(seq[2]):  # masses of signal
                massExcludedList = np.abs(filteredList - mof)
                # indexes = np.argwhere(massExcludedList == np.min(massExcludedList))[0] + 1
                indexes = np.unravel_index(massExcludedList.argmin(), massExcludedList.shape)
                out += f"{' '.join(str(v + 1) for v in indexes)}\n"
            # print(values)
            # print(temp - mof, mof)

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
    metabolite2('4.txt')
    # readFromPickle()
    end = time.time()
    print((end - start))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
