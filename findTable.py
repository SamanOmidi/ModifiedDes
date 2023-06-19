def permutation_table(binary_pairs):
    before, after = zip(*binary_pairs)
    
    size = len(before[0])

    table = [-1] * size

    for i in range(size):
        for j in range(size):
            if j in table:
                continue
            if all(after[k][i] == before[k][j] for k in range(len(binary_pairs))):
                table[i] = j
                break

    table = [x + 1 for x in table]
    return table

def find_table():
    f = open('output.txt', 'r')

    binary_pairs = []

    for line in f.readlines():
        line = line.strip()
        line = line.split(',')
        original = []
        permutated = []
        for bit in line[0]:
            original.append(int(bit))
        for bit in line[1]:
            permutated.append(int(bit))
        x = (original, permutated)
        binary_pairs.append(x)

    f.close()

    table = permutation_table(binary_pairs)
    
    return table