def lzw_encode(string_input):
    dictionary_size = 256  # 2^8 = 256; byte = string 8 bits
    dictionary = {
        chr(i): i for i in range(dictionary_size)
    }  # possible one-byte sequences

    # print(dictionary)
    encoding = []  # result
    current_code = ""  # index

    for symbol in string_input:
        if (
            current_code + symbol in dictionary
        ):  # if current_code + symbol exists in dictionary
            current_code += symbol  # update the current_code (index)
        else:
            encoding.append(
                dictionary[current_code]
            )  # add the code in the result array
            dictionary[current_code + symbol] = (
                dictionary_size  # store the new entry in the dictionary
            )
            dictionary_size += 1  # increase the dictionary size for future new entries
            current_code = symbol  # update the index

    if current_code:
        encoding.append(dictionary[current_code])

    return encoding


def lzw_decode(encoding):
    dictionary_size = 256  # 2^8 = 256; byte = string 8 bits
    dictionary = {
        i: chr(i) for i in range(dictionary_size)
    }  # possible one-byte sequences
    current_code = encoding[
        0
    ]  # initiliase the index with the first character from our encoding
    decoding = dictionary[current_code]  # store the first value in the result
    current_code = chr(current_code)  # transform the first character from int in char

    for code in encoding[1:]:  # continue with the rest chars of our encoding
        if code in dictionary:
            entry = dictionary[code]
        else:  # needed because sometimes the decoder may not yet have the entry
            entry = current_code + current_code[0]

        decoding += entry  # add entry to decoding result
        dictionary[dictionary_size] = (
            current_code + entry[0]
        )  # add the entry in dictionary
        current_code = entry  # update the index
        dictionary_size += 1

    return decoding


INPUT_DATA = "The decoding stage of this algorithm uses the received numerical codes and the same initial dictionary as in the encoding part (only that in this case the keys and values are switched), to translate these codes back into the original message. The algorithm can be seen in Algorithm"
input_encoding = lzw_encode(INPUT_DATA)
input_decoding = lzw_decode(input_encoding)
print(input_encoding)
print(input_decoding == INPUT_DATA)
