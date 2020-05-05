import argparse
import json
import string

ALPH_POWER = 26
# ------------- CAESER -----------------
def caeser_full(word, key, command) :
    alph = string.ascii_lowercase
    result = []

    for letter in word:
        if letter.isalpha():
            up_reg = 0
            if letter.isupper():
                up_reg = 1
            letter = letter.lower()
            pos = alph.find(letter)
            if (command == "encode") :
                new = (pos + key) % ALPH_POWER
            else :
                new = (pos - key + ALPH_POWER) % ALPH_POWER
            if up_reg == 1:
                result.append((alph[new]).upper())
            else :
                result.append(alph[new])
        else:
            result.append(letter)
    return result

def caeser_encode(word, key):
    res = caeser_full(word, key, "encode")

    r = ''.join(res)
    return r

def caeser_decode(code, key):
    dec_res = caeser_full(code, key, "decode")

    dec_r = ''.join(dec_res)
    return dec_r

# ------------- VIGENERE -----------------
def vig_dict():
    d = {}
    for i in range(len(string.ascii_lowercase)):
        d[i] = string.ascii_lowercase[i:i + 1]
    return d


def vig_encode_val(word):
    list_code = []
    register = []

    d = vig_dict()
    for cur_letter in word:
        if not cur_letter.isalpha():
            list_code.append([cur_letter, -1])
        else:
            if cur_letter.isupper():
                register.append(1)
            else:
                register.append(0)
            cur_letter = cur_letter.lower()
            for value in d:
                if cur_letter == d[value]:
                    list_code.append(value)
    list_code.append(register)

    return list_code

def vig_decode_val(list_in):
    list_code = []
    register = list_in[len(list_in) - 1]
    list_in.pop(len(list_in) - 1)

    d = vig_dict()

    i = 0
    for cur_letter in list_in:
        if not isinstance(cur_letter, str):
            for value in d:
                if cur_letter == value:
                    if register[i] == 1:
                        list_code.append(d[value].upper())
                    else:
                        list_code.append(d[value])
        else:
            list_code.append(cur_letter)
        i += 1

    return list_code


def vig_comparator(value, key):
    len_key = len(key) - 1
    dic = {}
    itr = 0
    full = 0
    for i in value:
        if isinstance(i, int):
            dic[full] = [i, key[itr]]
            full +=  1
            itr += 1
            if (itr >= len_key):
                itr = 0
        else:
            dic[full] = i
            full += 1

    return dic

def vig_full(value, key, command):
    dic = vig_comparator(value, key)
    d = vig_dict()
    register = dic[len(dic) - 1]
    dic.pop(len(dic) - 1)

    res = []
    for v in dic:
        if not isinstance(dic[v], str):
            if (command == "decode"):
                go = (dic[v][0] - dic[v][1] + len(d)) % len(d)
            else:
                go = (dic[v][0] + dic[v][1]) % len(d)
            res.append(go)
        else:
            res.append(dic[v])
    res.append(register)
    return res

def vig(word, key, command):
    key = key.lower()

    res = vig_decode_val(vig_full(vig_encode_val(word), vig_encode_val(key), command))
    r = ''.join(res)
    return r

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
    results = [0 for key in range(26)]
    main_key = 0
    begin = 0

    current_model = model(text)
    for key in range(ALPH_POWER):
        for letter in string.ascii_lowercase:
            cur_letter = string.ascii_lowercase[(string.ascii_lowercase.rfind(letter) + begin) % ALPH_POWER]
            results[key] += (main_model.get(letter, 0) - current_model.get(cur_letter, 0)) ** 2
        if results[key] < results[main_key]:
            main_key = key

        begin += 1

    return main_key

def hack_code(text, model):
    key = find_key(text, model)
    return caeser_decode(text, key)

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
        res = caeser_encode(text, key)
    else:
        key = args.key
        res = vig(text, key, "encode")
    write(args.output_file, res)


def decode(args):
    text = read(args.input_file)
    if args.cipher == "caesar":
        key = int(args.key)
        res = caeser_decode(text, key)
    else:
        key = args.key
        res = vig(text, key, "decode")
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
