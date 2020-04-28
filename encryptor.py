import argparse
import json
import string

ALPH_POWER = 26
# ------------- CAESER -----------------
def c_full(word, key, command) :
    alph = string.ascii_lowercase
    result = []
    for letter in word:
        if letter.isalpha():
            pos = alph.find(letter)
            if (command == "encode") :
                new = (pos + key) % ALPH_POWER
            else :
                new = (pos - key + ALPH_POWER) % ALPH_POWER
            result.append(alph[new])
        else:
            result.append(letter)
    return result


def c_full_encode(word, key):
    return c_full(word, key, "encode")

def c_full_decode(code, key):
    return c_full(code, key, "decode")

def c_find_key(txt):
    alph = string.ascii_lowercase
    max = 0
    symb = ''
    for letter in txt:
        count = 0
        for i in range(len(txt)):
            if letter == txt[i]:
                count += 1
        if count > max:
            max = count
            symb = letter
    return alph.find(symb)

def reg(word):
    register = []
    for v in word:
        if v.islower():
            register.append(0)
        else:
            register.append(1)
    return register

def c_encode(word, key):
    register = reg(word)

    word = word.lower()

    res = c_full_encode(word, key)

    i = 0
    for v in res:
        if register[i] == 1:
            res[i] = res[i].upper()
        i += 1
    r = ''.join(res)
    return r

def c_decode(code, key):
    register = reg(code)
    code = code.lower()
    dec_res = c_full_decode(code, key)

    for i in range(len(register)):
        if register[i] == 1:
            dec_res[i] = dec_res[i].upper()

    dec_r = ''.join(dec_res)
    return dec_r

# ------------- VIGENERE -----------------
def vig_dict():
    d = {}
    for i in range(97, 123):
        d[i - 97] = chr(i)
    return d


def vig_encode_val(word):
    list_code = []
    lent = len(word)

    d = vig_dict()
    for w in range(lent):
        if not word[w].isalpha():
            list_code.append(word[w])
        else:
            for value in d:
                if word[w] == d[value]:
                    list_code.append(value)
    return list_code


def vig_comparator(value, key):
    len_key = len(key)
    dic = {}
    iter = 0
    full = 0
    for i in value:
        if isinstance(i, int):
            dic[full] = [i, key[iter]]
            full +=  1
            iter += 1
            if (iter >= len_key):
                iter = 0
        else:
            dic[full] = i
            full += 1

    return dic

def vig_full(value, key, command):
    dic = vig_comparator(value, key)

    d = vig_dict()

    lis = []
    for v in dic:
        if not isinstance(dic[v], str):
            if (command == "decode"):
                go = (dic[v][0] - dic[v][1] + len(d)) % len(d)
            else:
                go = (dic[v][0] + dic[v][1]) % len(d)
            lis.append(go)
        else:
            lis.append(dic[v])

    return lis

def vig_full_encode(value, key):
    return vig_full(value, key, "encode")


def vig_full_decode(value, key):
    return vig_full(value, key, "decode")


def vig_decode_val(list_in):
    list_code = []
    lent = len(list_in)

    d = vig_dict()

    for i in range(lent):
        if not isinstance(list_in[i], str):
            for value in d:
                if list_in[i] == value:
                    list_code.append(d[value])
        else:
            list_code.append(list_in[i])
    return list_code


def reg(word):
    register = []
    for v in word:
        if v.islower():
            register.append(0)
        else:
            register.append(1)
    return register

def vig(word, key, command):
    register = reg(word)
    word = word.lower()
    key = key.lower()

    if (command == "encode"):
        res = vig_decode_val(vig_full_encode(vig_encode_val(word), vig_encode_val(key)))
    else:
        res = vig_decode_val(vig_full_decode(vig_encode_val(word), vig_encode_val(key)))
    for i in range(len(register)):
        if register[i] == 1:
            res[i] = res[i].upper()
    r = ''.join(res)
    return r

def vig_encode(word, key):
    return vig(word, key, "encode")


def vig_decode(code, key):
    return vig(code, key, "decode")

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

    current_model = model(text)
    for key in range(ALPH_POWER):
        for letter in string.ascii_lowercase:
            results[key] += (main_model.get(letter, 0) - current_model.get(letter, 0)) ** 2
        if results[key] < results[main_key]:
            main_key = key

        zero = current_model[string.ascii_lowercase[0]]
        for i in range(ALPH_POWER - 1):
            current_model[string.ascii_lowercase[i]] = current_model[string.ascii_lowercase[i + 1]]
        current_model[ALPH_POWER - 1] = zero

    return main_key

def hack_code(text, model):
    key = find_key(text, model)
    return c_decode(text, key)

# ------------- MAIN ------------------

def Read(input_file):
    if input_file is None:
        text = input()
    else:
        text = input_file.read()
    return text

def Write(output_file, res):
    if output_file is None:
        print(res)
    else:
        output_file.write(res)

def encode(args):
    if args.cipher == "caesar":
        key = int(args.key)
        text = Read(args.input_file)
        res = c_encode(text, key)
        Write(args.output_file, res)
    else:
        key = args.key
        text = str(args.input_file)
        res = vig_encode(text, key)
        Write(args.output_file, res)


def decode(args):
    if args.cipher == "caesar":
        key = int(args.key)
        if args.input_file is None:
            text = input()
        else:
            text = str(args.input_file.read())
        res = c_decode(text, key)
        if args.output_file is None:
            print(res)
        else:
            args.output_file.write(res)
    else:
        key = args.key
        code = Read(args.input_file)
        res = vig_decode(code, key)
        Write(args.output_file, res)


def train(args):
    text = Read(args.text_file)
    args.model_file.write(train_txt(text))


def hack(args):
    model = json.load(args.model_file)
    text = Read(args.input_file)
    res = hack_code(text, model)
    Write(args.output_file, res)


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
