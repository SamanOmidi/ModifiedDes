# initial values
#######################################################
def pad(text):
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    return text + padding


# parity bit drop table
PARITY_DROP = [57, 49, 41, 33, 25, 17, 9, 1,
               58, 50, 42, 34, 26, 18, 10, 2,
               59, 51, 43, 35, 27, 19, 11, 3,
               60, 52, 44, 36, 63, 55, 47, 39,
               31, 23, 15, 7, 62, 54, 46, 38,
               30, 22, 14, 6, 61, 53, 45, 37,
               29, 21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts
SHIFT_TABLE = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

# Key Compression Table 
KEY_COMP = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]

# Initial Permutation Table
INIT_PERM = [58, 50, 42, 34, 26, 18, 10, 1,
             60, 52, 44, 36, 28, 20, 12, 4,
             62, 54, 46, 38, 30, 22, 14, 6,
             64, 56, 48, 40, 32, 24, 16, 8,
             57, 49, 41, 33, 25, 17, 9, 2,
             59, 51, 43, 35, 27, 19, 11, 3,
             61, 53, 45, 37, 29, 21, 13, 5,
             63, 55, 47, 39, 31, 23, 15, 7]

# Expansion P-box Table
EXP_P_BOX = [32, 1, 2, 3, 4, 5, 4, 5,
             6, 7, 8, 9, 8, 9, 10, 11,
             12, 13, 12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21, 20, 21,
             22, 23, 24, 25, 24, 25, 26, 27,
             28, 29, 28, 29, 30, 31, 32, 1]

# S-box Table
S_BOX = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
          [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
          [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
          [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
          [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

         [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
          [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
          [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
          [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

         [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
          [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
          [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
          [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

         [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
          [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
          [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
          [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

         [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
          [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
          [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
          [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

         [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
          [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
          [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
          [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

         [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
          [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
          [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
          [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutation Table
FINAL_PERM = [8, 40, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

plain_cipher = [
    ['kootahe','6E2F7B25307C3144'],
    ['Zendegi','CF646E7170632D45'],
    ['Edame'  ,'D070257820560746'],
    ['Dare'   ,'5574223505051150'],
    ['JolotYe','DB2E393F61586144'],
    ['Daame'  ,'D175257820560746'],
    ['DaemKe' ,'D135603D1A705746'],
    ['Mioftan','D83C6F7321752A54'],
    ['Toosh'  ,'413A2B666D024747'],
    ['HattaMo','5974216034186B44'],
    ['khayeSa','EA29302D74463545'],
    ['05753jj','B1203330722B7A04'],
    ['==j95697','38693B6824232D231D1C0D0C4959590D']]
#######################################################


# DES initial permutation
def initial_permuation(input_text):
    # convert it to binary
    text = bin(int(input_text, 16))[2:]
    # add zero if less than 64 length
    text = '{:064b}'.format(int(text, 2))
    
    result = ''
    for i in INIT_PERM:
        result += text[i-1]
    
    return result

# DES final permutation
def final_permuation(input_text):
    result = ''
    for i in FINAL_PERM:
        result += input_text[i-1]
    
    return result

# DES key generator
KEY = '4355262724562343'
def one_round_key():
    # convert key to binary
    key = bin(int(KEY, 16))[2:]
    # add zero if less than 64 length
    key = '{:064b}'.format(int(key, 2))
    
    result = ''
    for i in PARITY_DROP:
        result += key[i-1]
    
    left_key, right_key = result[:len(result) // 2], result[len(result) // 2:]
    
    # do 1 cirular shift
    left_key = left_key[1:] + left_key[0]
    right_key= right_key[1:] + right_key[0]
    
    key = ''
    key = left_key + right_key

    result = ''
    for i in KEY_COMP:
        result += key[i-1]

    return result

# DES function
def function(right_plain_text):
    # make the key
    key = one_round_key()

    # step 1 -> expansion P-box
    expansion_pbox_result = ''
    for i in EXP_P_BOX:
        expansion_pbox_result += right_plain_text[i-1]
    
    # step 2 -> xor expansion_pbox_result with key
    xor_result = ''
    xor_result = bin(int(expansion_pbox_result, 2) ^ int(key, 2))[2:]
    # add zeros to the beginning
    xor_result = '{:048b}'.format(int(xor_result, 2))

    # step 3 -> S-Boxes
    sbox_result = ''
 
    for i, j in enumerate(list(range(0, 48, 6))):
        # determine 6 bits that goes to s-box
        six_bits = xor_result[j: j+6]
        # determine s-box
        sbox = S_BOX[i]

        # determine s-box row and col
        col_index = int(six_bits[1:5], 2)
        row_index = int(six_bits[0] + six_bits[5], 2)

        answer = bin(sbox[row_index][col_index])[2:]
        # add zeros
        answer = '{:04b}'.format(int(answer, 2))

        sbox_result += answer
    
    return sbox_result

# DES encrypt
def des(plain_text, cipher_text):
    # determine plaintext
    plain_text = plain_text.encode('utf-8').hex()
    
    plain_text = initial_permuation(plain_text)
    
    cipher_text = initial_permuation(cipher_text)

    left_cipher_text = cipher_text[:len(cipher_text) // 2]
    right_cipher_text = cipher_text[len(cipher_text) // 2:]

    left_plain_text = plain_text[:len(plain_text) // 2]
    right_plain_text = plain_text[len(plain_text) // 2:]
    
    # result before straight p-box
    before_straight_pbox = function(right_plain_text)

    # result after startigh p-box
    temp = bin(int(left_cipher_text, 2) ^ int(left_plain_text, 2))[2:]
    temp = '{:032b}'.format(int(temp, 2))
    after_straight_pbox = temp
    
    return before_straight_pbox, after_straight_pbox

# DES decrypt
def decrypt(table):
    cipher_text = input()
    plain_text = ''
    for i in range(0, len(cipher_text), 16):
        text = cipher_text[i: i+16]
        
        text = initial_permuation(text)
        left , right = text[:len(text) // 2], text[len(text) // 2:]
        before_straight_pbox = function(right)

        result = ''
        for i in table:
            result += before_straight_pbox[i-1]

        left = bin(int(result, 2) ^ int(left, 2))[2:]
        left = '{:032b}'.format(int(left, 2))
        
        answer = left + right
        # do final permutation
        answer = final_permuation(answer)
        # convert to hex and remove 0x
        answer = hex(int(answer, 2))[2:]
        answer = "{:016x}".format(int(answer, 16))
        # convert hex to ascii
        answer = bytes.fromhex(answer).decode('utf-8')

        plain_text += answer
    plain_text = plain_text[:24]
    print(plain_text)

# Convert bin to string
def bin_to_str(my_bin):
    my_int = my_int = int(my_bin, base=2)
    my_str = my_int.to_bytes((my_int.bit_length() + 7)//8, 'big').decode()
    return my_str

# Find Permutation Table       
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


def main():
    binary_pairs = []
    for line in plain_cipher:
        plain_text = line[0]
        cipher_text = line[1]

        plain_text = pad(plain_text)
        if len(plain_text) > 8:
            plain_text_first = plain_text[:len(plain_text) // 2]
            plain_text_second = plain_text[len(plain_text) // 2:]
            cipher_text_first = cipher_text[:len(cipher_text) // 2]
            cipher_text_second = cipher_text[len(cipher_text) // 2:]

            before_straight_pbox_first, after_straight_pbox_first = des(plain_text_first, cipher_text_first)
            before_straight_pbox_second, after_straight_pbox_second = des(plain_text_second, cipher_text_second)
            x = (before_straight_pbox_first, after_straight_pbox_first)
            binary_pairs.append(x)
            x = (before_straight_pbox_second, after_straight_pbox_second)
            binary_pairs.append(x)
        else:
            before_straight_pbox, after_straight_pbox = des(plain_text, cipher_text)
            x = (before_straight_pbox, after_straight_pbox)
            binary_pairs.append(x)

    table = permutation_table(binary_pairs)

    decrypt(table)
if __name__ == '__main__':
    main()