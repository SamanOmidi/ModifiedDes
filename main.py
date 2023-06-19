import boxes
import pad
import findTable

def initial_permuation(input_text):
    # convert it to binary
    text = bin(int(input_text, 16))[2:]
    # add zero if less than 64 length
    text = '{:064b}'.format(int(text, 2))
    
    result = ''
    for i in boxes.INIT_PERM:
        result += text[i-1]
    
    return result

def final_permuation(input_text):
    result = ''
    for i in boxes.FINAL_PERM:
        result += input_text[i-1]
    
    return result

KEY = '4355262724562343'
def one_round_key():
    # convert key to binary
    key = bin(int(KEY, 16))[2:]
    # add zero if less than 64 length
    key = '{:064b}'.format(int(key, 2))
    
    result = ''
    for i in boxes.PARITY_DROP:
        result += key[i-1]
    
    left_key, right_key = result[:len(result) // 2], result[len(result) // 2:]
    
    # do 1 cirular shift
    left_key = left_key[1:] + left_key[0]
    right_key= right_key[1:] + right_key[0]
    
    key = ''
    key = left_key + right_key

    result = ''
    for i in boxes.KEY_COMP:
        result += key[i-1]

    return result


def function(right_plain_text):
    # make the key
    key = one_round_key()

    # step 1 -> expansion P-box
    expansion_pbox_result = ''
    for i in boxes.EXP_P_BOX:
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
        sbox = boxes.S_BOX[i]

        # determine s-box row and col
        col_index = int(six_bits[1:5], 2)
        row_index = int(six_bits[0] + six_bits[5], 2)

        answer = bin(sbox[row_index][col_index])[2:]
        # add zeros
        answer = '{:04b}'.format(int(answer, 2))

        sbox_result += answer
    
    return sbox_result

def bin_to_str(my_bin):
    ''' Converts a Binary String to an (ASCII) string'''
    my_int = my_int = int(my_bin, base=2)
    my_str = my_int.to_bytes((my_int.bit_length() + 7)//8, 'big').decode()
    return my_str

def decrypt(table):
    cipher_text = '59346E29456A723B62354B61756D44257871650320277C741D1C0D0C4959590D'
    plait_text = ''
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

        plait_text += answer

    f = open('answer.txt', 'w')
    to_write = ''
    to_write += 'Table: ' + ''.join(str(x) + ',' for x in table) + '\n' + 'Plain_Text: ' + plait_text
    f.write(to_write)
    f.close()


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
       

def main():
    # read from file
    f = open('pair.txt', 'r')
    outputFile = open('output.txt', 'w')

    for line in f.readlines():
        line = line.strip()
        if line == 'plain & Cipher:{':
            continue
        elif line[0] == '}':
            break
        else:
            temp = line.split(',')
            plain_text = temp[0]
            cipher_text = temp[1]
            
            plain_text = pad.pad(plain_text)

            if len(plain_text) > 8:
                plain_text_first = plain_text[:len(plain_text) // 2]
                plain_text_second = plain_text[len(plain_text) // 2:]
                cipher_text_first = cipher_text[:len(cipher_text) // 2]
                cipher_text_second = cipher_text[len(cipher_text) // 2:]

                before_straight_pbox_first, after_straight_pbox_first = des(plain_text_first, cipher_text_first)
                before_straight_pbox_second, after_straight_pbox_second = des(plain_text_second, cipher_text_second)
                outputFile.write(before_straight_pbox_first + ',' + after_straight_pbox_first + '\n')
                outputFile.write(before_straight_pbox_second + ',' + after_straight_pbox_second + '\n')
            else:
                before_straight_pbox, after_straight_pbox = des(plain_text, cipher_text)
                outputFile.write(before_straight_pbox + ',' + after_straight_pbox + '\n')

    f.close()
    outputFile.close()
   
    table = findTable.find_table()
    decrypt(table)
if __name__ == '__main__':
    main()