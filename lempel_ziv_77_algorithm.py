def lz77_encode(text, search_buffer_size=256):
    position = 0
    encoding = []

    # slide the window over the text
    while position < len(text):
        # initialize the length and offset of the longest match
        best_offset = 0
        biggest_length = 0

        # move the offset value from left to right
        for offset in range(1, min(search_buffer_size, position) + 1):
            if position - offset < 0:
                continue

            # initialize the length of the match starting at the current offset
            length = 0

            # increase the length while the corresponding character from the search and look-ahead buffers are equal
            while text[position - offset + length] == text[position + length]:
                length += 1

                # treat the cases when characters outside the search buffer or text are accessed
                if position + length >= len(text) or length >= offset:
                    break

            # update the length and offset of the longest match
            if length > biggest_length:
                biggest_length = length
                best_offset = offset

        # treat the case when the next character after the match is the end of the string
        if position + biggest_length >= len(text):
            next_character = ""
        else:
            next_character = text[position + biggest_length]

        # add in the encoding of the current triplet
        encoding.append((best_offset, biggest_length, next_character))

        # move the look-ahead buffer
        position += biggest_length + 1

    return encoding


def lz77_decode(encoded_text):
    # initialize the reconstructed text 
    reconstructed_text = ""

    # iterate over each triplet
    for offset, length, character in encoded_text:

        # reconstruct the text
        if length == 0:
            reconstructed_text += character
        else:
            reconstructed_text += reconstructed_text[-offset:][:length] + character

    return reconstructed_text


if __name__ == "__main__":
    text = """This is a test text."""
    encoded_text = lz77_encode(text)
    print(encoded_text)
    reconstructed_text = lz77_decode(encoded_text)
    print(reconstructed_text)
    assert text == reconstructed_text, "Reconstruction error"
