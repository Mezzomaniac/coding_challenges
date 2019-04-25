target = (2978, 3083)

def seqn(row, col):
    subseq = row + col - 1
    subseq1 = (subseq ** 2 - subseq + 2) // 2
    return subseq1 + col - 1

def code(seqn):
    result = 20151125
    for i in range(seqn - 1):
        result = (result * 252533) % 33554393
    return result

print(code(seqn(*target)))
