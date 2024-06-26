import sys
import json
import time
import pandas as pd
from lempel_ziv_77_algorithm import lz77_encode, lz77_decode
from lempel_ziv_welch_algorithm import lzw_encode, lzw_decode


def load_data(type):
    with open("./data/texts.json", encoding="utf-8") as f:
        data = json.load(f)
        texts = data[type]
    return texts


def get_number_of_bytes(encoding, encoding_algorithm=None):
    if encoding_algorithm == "lz77":
        return (4 + 4 + 1) * len(encoding)
    elif encoding_algorithm == "lzw":
        return 4 * len(encoding)
    else:
        return len(encoding)


def perform_measurements(texts, text_type, number_of_repetitions=100):
    lz77_encoding_times = []
    lz77_decoding_times = []
    lzw_encoding_times = []
    lzw_decoding_times = []
    lz77_compression_rates = []
    lzw_compression_rates = []
    text_sizes = []

    for _, text in enumerate(texts):
        text_ascii = text.encode("ascii", "ignore").decode()
        lz77_encoding_time = 0
        lz77_decoding_time = 0
        lzw_encoding_time = 0
        lzw_decoding_time = 0

        for index in range(number_of_repetitions):
            start_time = time.time()
            lz77_encoded_text = lz77_encode(text_ascii, search_buffer_size=sys.maxsize)
            lz77_encoding_time += time.time() - start_time

            start_time = time.time()
            lz77_decoded_text = lz77_decode(lz77_encoded_text)
            lz77_decoding_time += time.time() - start_time

            start_time = time.time()
            lzw_encoded_text = lzw_encode(text_ascii)
            lzw_encoding_time += time.time() - start_time

            start_time = time.time()
            lzw_decoded_text = lzw_decode(lzw_encoded_text)
            lzw_decoding_time += time.time() - start_time

            if index == 0:
                assert text_ascii == lz77_decoded_text
                assert text_ascii == lzw_decoded_text

                initial_size = get_number_of_bytes(text_ascii)
                text_sizes.append(initial_size)
                lz77_encoding_size = get_number_of_bytes(lz77_encoded_text, "lz77")
                lzw_encoding_size = get_number_of_bytes(lzw_encoded_text, "lzw")

                lz77_compression_rates.append(initial_size / lz77_encoding_size * 100)
                lzw_compression_rates.append(initial_size / lzw_encoding_size * 100)

        lz77_encoding_times.append(lz77_encoding_time / number_of_repetitions)
        lz77_decoding_times.append(lz77_decoding_time / number_of_repetitions)
        lzw_encoding_times.append(lzw_encoding_time / number_of_repetitions)
        lzw_decoding_times.append(lzw_decoding_time / number_of_repetitions)

        recorded_measuremets = pd.DataFrame(
            {
                "text_sizes": text_sizes,
                "LZ77 encoding time": lz77_encoding_times,
                "LZ77 decoding time": lz77_decoding_times,
                "LZ77 compression rates": lz77_compression_rates,
                "LZW encoding time": lzw_encoding_times,
                "LZW decoding time": lzw_decoding_times,
                "LZW compression rates": lzw_compression_rates,
            }
        )

        recorded_measuremets.to_csv(f"./data/measurents_{text_type}.csv")


if __name__ == "__main__":
    types_of_texts = [
        "lorem_ipsum_texts",
        "english_literature_texts",
        "programming_source_code",
    ]
    type_index = 2

    texts = load_data(types_of_texts[type_index])
    perform_measurements(texts, types_of_texts[type_index], number_of_repetitions=1)
