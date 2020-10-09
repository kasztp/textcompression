# Name:         Text Compression Service v0.5
# Maintainer:   Peter Kaszt (peter@talentstack.eu)
# Date:         2020.10.08.
#
# Usage:    Run the app as standalone if you have Flask installed.
#           Modify host parameter for flask according to your needs.
#           Remove debug=True for production!
import sys
import itertools

from flask import Flask, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nobody-gonna-guess-it'


def compress(data):
    original_length = len(data)
    text = list()
    # Split text into lines and text
    for line in data.splitlines(keepends=True):
        text.append(line.split())
    print(f"Text lines: {len(text)}")
    print(text)
    # Generate word dictionaries for compression & decompression
    unique_words = list(set(itertools.chain(*text)))
    for word in unique_words:
        if len(word) <= 2:
            unique_words.remove(word)
    unique_words.sort(key=len)
    print(unique_words)
    extract_dict = dict()
    compress_dict = dict()
    for index, word in enumerate(unique_words):
        #print(f"Index: {index}  -  Word: {word}")
        extract_dict[str(index)] = word
        compress_dict[word] = str(index)
    print(f"Compress dictionary size: {len(compress_dict)}")
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
    # Prepare response
    result = {
        "original_length": original_length,
        "compressed_length": compressed_length,
        "dictionary": extract_dict,
        "text": compressed_text
    }
    return result


def extract(data):
    # Extract original text
    extract_dict = data["payload"]["dictionary"]
    #print(type(extract_dict))
    compressed_text = data["payload"]["text"]
    print(f"Compressed text: {compressed_text}")
    keys = list()
    for key in extract_dict.keys():
        keys.append(int(key))
    for key in sorted(keys, reverse=True):
        value = extract_dict.get(str(key))
        #print(f"{key} : {value}")
        compressed_text = compressed_text.replace(str(key), value)
    print(f"Decompressed text: {compressed_text}")
    # Prepare response
    result = {
        "original_length": data["original_length"],
        "text": compressed_text
    }
    return result


@app.route('/', methods=['GET', 'POST'])
def home():
    return '''<h1>Sorting Service</h1>
<p>Input example for text:</p>
<p>
{
  "mode": "compress",
  "payload": "input text"
}
</p>

<p>Input example for data:</p>
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
</p>'''


@app.route('/compress', methods=['GET', 'POST'])
def sort():
    data = request.get_json(silent=True)
    request_size = request.content_length
    request_json_size = sys.getsizeof(request.get_json(silent=True))
    print(f"Incoming request size: {request_size}")
    print(f"Incoming JSON size: {request_json_size}")
    print(f"Incoming request:\n{data}")
    mode = data['mode']
    print(f"\nRequest type: {mode}")
    if mode == "compress":
        response = compress(data['payload'])
    elif mode == "extract":
        response = extract(data)
    else:
        response = "Wrong mode! Only compress/extract are supported."
    print(f"Response:\n{response}")
    print(f"Response size: {sys.getsizeof(response)}")
    return response


if __name__ == '__main__':
    app.run(debug=True)
