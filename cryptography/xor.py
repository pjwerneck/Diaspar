
# coding: UTF-8

import itertools
import sys
import random
from pprint import pprint


WORDS = [line.strip() for line in open('commonwords')]


#realkey = "kop\deft(olgqa]x"


def f(text, key):
    # Esta é a função de encriptação, faz o xor com cada byte
    for a, b in zip(text, itertools.cycle(key)):
        yield chr(ord(a) ^ ord(b))

def asc2hex(data):
    # converte de ASCII para hexadecimal, para facilitar a visualização
    return ''.join('%02x'%ord(c) for c in data)

def split_blocks(data, size):
    # esta função apenas divide o texto em blocos do tamanho da chave
    n = len(data)
    for i, j in zip(xrange(0, n, size), xrange(size, n+1, size)):
        yield ''.join(data[i:j])
    yield ''.join(data[j:])


ctext = list(split_blocks(asc2hex(open('ciphertext').read()), 2))
print ctext

d = []
for block in list(split_blocks(ctext, 16)):
    print block
    
