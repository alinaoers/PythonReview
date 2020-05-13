import argparse
import json
import string

ALPH_POWER = len(string.ascii_lowercase)
# ------------- CAESAR -----------------
def caesar(word, key, command) :
    alph = string.ascii_lowercase
    result = []

    for letter in word:
        if letter.isalpha():
            up = False
            if letter.isupper():
                up = True
            letter = letter.lower()
            pos = alph.find(letter)
            if (command == "encode") :
                new = (pos + key) % ALPH_POWER
            else :
                new = (pos - key + ALPH_POWER) % ALPH_POWER
            if up:
                result.append((alph[new]).upper())
            else :
                result.append(alph[new])
        else:
            result.append(letter)
    return ''.join(result)

def caesar_encode(word, key):
    return caesar(word, key, "encode")

def caesar_decode(code, key):
    return caesar(code, key, "decode")

# ------------- VIGENERE -----------------

def vig(key, text, command):
    result = []
    symb = 0
    for index, ch in enumerate(text):
        if ch.isalpha():
            up = False
            if ch.isupper():
                up = True
                ch = ch.lower()
            from_dict = string.ascii_lowercase.index(ch)
            from_key = string.ascii_lowercase.index(key[(index - symb + len(key)) % len(key)])
            if (command == "decode"):
                cur_idx = (from_dict - from_key + ALPH_POWER) % ALPH_POWER
            else:
                cur_idx = (from_dict + from_key) % ALPH_POWER
            if up:
                result.append(string.ascii_lowercase[cur_idx].upper())
            else:
                result.append(string.ascii_lowercase[cur_idx])
        else:
            symb += 1
            result.append(ch)
    print(result)
    return ''.join(result)

def vig_decode(key,text):
    return vig(key.lower(), text, "decode")


def vig_encode(key, text):
    return vig(key.lower(), text, "encode")

# ------------ TRAIN ------------------
def model(text):
    count = {}
    letter_count = 0
    for symbol in text.lower():
        if symbol.isalpha():
            count[symbol] = count.get(symbol, 0) + 1
            letter_count += 1

    result = {}
    for letter in string.ascii_lowercase:
        result[letter] = float(count.get(letter, 0)) / float(letter_count)
    return result

def train_txt(text):
    result = model(text)
    return json.dumps(result)

# ------------ HACK --------------------
def find_key(text, main_model):
    main_key = 0
    begin = 0
    min_res = ALPH_POWER
    current_model = model(text)

    for key in range(ALPH_POWER):
        cur_result = 0;
        for letter in string.ascii_lowercase:
            cur_letter = string.ascii_lowercase[(string.ascii_lowercase.rfind(letter) + begin) % ALPH_POWER]
            cur_result += (main_model.get(letter, 0) - current_model.get(cur_letter, 0)) ** 2
        if cur_result < min_res:
            main_key = key
            min_res = cur_result

        begin += 1

    return main_key

def hack_code(text, model):
    key = find_key(text, model)
    return caesar_decode(text, key)

# ------------- MAIN ------------------

def read(input_file):
    if input_file is None:
        text = input()
    else:
        text = input_file.read()
    return text

def write(output_file, res):
    if output_file is None:
        print(res)
    else:
        output_file.write(res)

def encode(args):
    text = read(args.input_file)
    if args.cipher == "caesar":
        key = int(args.key)
        res = caesar_encode(text, key)
    else:
        key = args.key
        res = vig_encode(key, text)
    write(args.output_file, res)



def decode(args):
    text = read(args.input_file)
    if args.cipher == "caesar":
        key = int(args.key)
        res = caesar_decode(text, key)
    else:
        key = args.key
        res = vig_decode(key, text)
    write(args.output_file, res)


def train(args):
    text = read(args.text_file)
    args.model_file.write(train_txt(text))


def hack(args):
    model = json.load(args.model_file)
    text = read(args.input_file)
    res = hack_code(text, model)
    write(args.output_file, res)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


parser_encode = subparsers.add_parser('encode')
parser_encode.set_defaults(mode='encode', func=encode)
parser_encode.add_argument('--cipher', choices=['caesar', 'vigenere'])
parser_encode.add_argument('--key')
parser_encode.add_argument('--input-file', type=argparse.FileType('r'))
parser_encode.add_argument('--output-file', type=argparse.FileType('w'))


parser_decode = subparsers.add_parser('decode')
parser_decode.set_defaults(mode='decode', func=decode)
parser_decode.add_argument('--cipher', choices=['caesar', 'vigenere'])
parser_decode.add_argument('--key')
parser_decode.add_argument('--input-file', type=argparse.FileType('r'))
parser_decode.add_argument('--output-file', type=argparse.FileType('w'))


parser_train = subparsers.add_parser('train')
parser_train.set_defaults(mode='train', func=train)
parser_train.add_argument('--text-file', type=argparse.FileType('r'))
parser_train.add_argument('--model-file', type=argparse.FileType('w'))


parser_hack = subparsers.add_parser('hack')
parser_hack.set_defaults(mode='hack', func=hack)
parser_hack.add_argument('--input-file', type=argparse.FileType('r'))
parser_hack.add_argument('--output-file', type=argparse.FileType('w'))
parser_hack.add_argument('--model-file', type=argparse.FileType('r'))


arguments = parser.parse_args()
arguments.func(arguments)
