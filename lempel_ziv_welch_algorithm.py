def lzw_encode(string_input):
    dictionary_size = 256  # 2^8 = 256; byte = string 8 bits
    dictionary = {
        chr(i): i for i in range(dictionary_size)
    }  # possible one-byte sequences
    encoding = []
    current_code = ""

    for symbol in string_input:
        if current_code + symbol in dictionary:
            current_code += symbol
        else:
            encoding.append(dictionary[current_code])
            dictionary[current_code + symbol] = dictionary_size
            dictionary_size += 1
            current_code = symbol

    if current_code:
        encoding.append(dictionary[current_code])

    return encoding


def lzw_decode(encoding):
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}
    current_code = encoding[0]
    decoding = dictionary[current_code]
    current_code = chr(current_code)

    for code in encoding[1:]:
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = current_code + current_code[0]

        decoding += entry
        dictionary[dictionary_size] = current_code + entry[0]
        current_code = entry
        dictionary_size += 1

    return decoding


INPUT_DATA = "abcabcabcabcabcabcabcabcabcabcabcabc"
input_encoding = lzw_encode(INPUT_DATA)
input_decoding = lzw_decode(input_encoding)
print(input_decoding == INPUT_DATA)
