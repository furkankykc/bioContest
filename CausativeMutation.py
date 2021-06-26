import numpy as np

nt = {
    'A': 17,
    'T': 19,
    'G': 13,
    'C': 11
}
neg = []
pos = []


def mutation(fileName):
    with open(f'final_data/{fileName}') as file:
        lines = [line.rstrip() for line in file]
        numberOfTests = int(lines[0])
        i = 1
        iterator = 0
        out = ""
        while iterator < numberOfTests:
            # print(i, '|', lines[i])
            numberOfCases, lengthOfCases = tuple(int(x) for x in lines[i].split(' '))
            # seq = []

            print(numberOfCases)

            for j in range(i + 1, i + 2 * (numberOfCases) + 1, 2):
                # print(lines[j])
                # print(numberOfCases, lengthOfCases, numberOfTests)
                # seq[lines[j]] = list(lines[j + 1])
                if lines[j] == '+':
                    pos.append(list(map(lambda x: nt[x], list(lines[j + 1]))))
                else:
                    neg.append(list(map(lambda x: nt[x], list(lines[j + 1]))))
            # print(numpy.transpose(seq))
            res = freq(pos)
            out += f"{res[0]} {res[1]}\n"
            print(out)
            i = i + numberOfCases + 1
            iterator += 1
        # print(pos)
        # print(neg)
        f = open(f'final_res/res_{fileName}', 'w')
        f.write(out)  # python will convert \n to os.linesep
        f.close()  #


def freq(seq: list) -> (int, int):
    len_seq = len(seq)
    transposed = np.transpose(seq)
    col_seq = len(seq[0])
    for i in range(0, len_seq):
        for j in range(0, len_seq):
            arr = transposed[i:len_seq - j]
            seq_sum = np.divide(np.sum(arr), len(arr))
            # seq_mul = np.prod(seq_sum % list(nt.values()))
            seq_sub = np.subtract(seq_sum, list(nt.values()))
            seq_mul = np.prod(seq_sub)
            if seq_mul == 0:
                return i, len_seq - j - 1

    return 0, col_seq - 1


if __name__ == '__main__':
    mutation('problem2/01')
