# Name:         Text Compression Service v0.6
# Maintainer:   Peter Kaszt (peter@talentstack.eu)
# Date:         2021.01.12.
#
# Usage:    Run the app as standalone if you have Flask installed.
#           Modify host parameter for flask according to your needs.
#           Remove debug=True for production!
import sys
import itertools
import requests
from validator_collection import checkers
from flask import Flask, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "nobody-gonna-guess-it"


def base_x(number):
    b_x = str()
    digits = '0123456789AÁBCDEÉFGHIÍJKLMNOÓÖŐPQRSTUÚÜŰVWXYZaábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz'
    while number != 0:
        number, i = divmod(number, len(digits))
        b_x = digits[i] + b_x
    return b_x


def pack(payload, input_type):
    if input_type == "url":
        response = requests.request("GET", payload, allow_redirects=True)
        status_code = response.status_code  # to be used for tests.
        data = response.text
    else:
        data = payload
        # print(data)
    original_length = len(data)
    print(f"Downloaded text size: {original_length}")
    text = list()
    # Split text into lines and text
    for line in data.splitlines(keepends=True):
        text.append(line.split())
    print(f"Text lines: {len(text)}")
    # print(text)
    # Generate word dictionaries for compression & decompression
    unique_words = list(set(itertools.chain(*text)))
    for word in unique_words:
        if len(word) <= 2:
            unique_words.remove(word)
    unique_words.sort(key=len)
    # print(unique_words)
    extract_dict = dict()
    compress_dict = dict()
    for index, word in enumerate(unique_words):
        # print(f"Index: {index}  -  Word: {word}")
        extract_dict[str(hex(index))[2:]] = word
        compress_dict[word] = base_x(index)
    dictionary_length = sys.getsizeof(compress_dict)
    print(f"Compress dictionary size: {dictionary_length}")
    # Compress text
    for row, line in enumerate(text):
        for column, word in enumerate(line):
            if word in compress_dict:
                text[row][column] = compress_dict[word]
    # Convert compressed list to text
    for row, line in enumerate(text):
        separator = " "
        text[row] = separator.join(line)
    separator = "\n"
    compressed_text = separator.join(text)
    compressed_length = len(compressed_text)
    print(f"Compressed text size: {compressed_length}")
    # Prepare response
    result = {
        "original_length": original_length,
        "compressed_length": compressed_length,
        "dictionary": extract_dict,
        "dictionary_length": dictionary_length,
        "text": compressed_text
    }
    return result


def extract(data):
    # Extract original text
    extract_dict = data["payload"]["dictionary"]
    # print(type(extract_dict))
    compressed_text = data["payload"]["text"]
    print(f"Compressed text: {compressed_text}")
    keys = list()
    for key in extract_dict.keys():
        keys.append(int(key))
    for key in sorted(keys, reverse=True):
        value = extract_dict.get(str(key))
        # print(f"{key} : {value}")
        compressed_text = compressed_text.replace(str(key), value)
    print(f"Decompressed text: {compressed_text}")
    # Prepare response
    result = {
        "original_length": data["original_length"],
        "text": compressed_text
    }
    return result


@app.route("/", methods=["GET", "POST"])
def home():
    return """<h1>Text Compression Service</h1>
<p>Input example for text:</p>
<p>
{
  "mode": "compress",
  "payload": "input text"
}
</p>
--------------------------------------
<p>Input example for url:</p>
<p>
{
  "mode": "compress",
  "payload": "url"
}
</p>
--------------------------------------
<p>Input example for compressed data:</p>
<p>
{
  "mode": "extract",
  "original_length": original_length,
  "payload": {
        "dictionary": {
            "0": "data",
            "1": "compressed",
        "text": "1 \n0"
        }
}
</p>"""


@app.route("/compress", methods=["GET", "POST"])
def compress():
    data = request.get_json(silent=True)
    request_size = request.content_length
    request_json_size = sys.getsizeof(request.get_json(silent=True))

    print(f"Incoming request size: {request_size}")
    print(f"Incoming JSON size: {request_json_size}")
    # print(f"Incoming request:\n{data}")
    mode = data["mode"]
    print(f"\nRequest type: {mode}")
    if mode == "compress":
        if checkers.is_url(data["payload"]):
            response = pack(data["payload"], "url")
        else:
            response = pack(data["payload"], "text")
    elif mode == "extract":
        response = extract(data)
    else:
        response = "Wrong mode! Only compress/extract are supported."
    # print(f"Response:\n{response}")
    print(f"Response size: {sys.getsizeof(response)}")
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
