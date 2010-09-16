

import random

text = open("plaintext").read()


def xor(a, b):
    return "".join(chr(ord(x) ^ ord(y) ) for x, y in zip(a, b))


def split(data, n):
    size = len(data)
    for i, j in zip(xrange(0, size, n), xrange(n, size+1, n)):
        yield data[i:j]
    if j < size:
        yield data[j:].ljust(n, chr(0))  


def build_iv(n):
    return "".join(chr(random.randint(0, 255)) for x in xrange(n))

def asc2hex(data):
    return ''.join('%02x'%ord(c) for c in data)


def cbc(data, key):
    blocksize = len(key)
    out = [build_iv(blocksize)]
    for block in split(data, blocksize):
        block = xor(block, out[-1])
        block = xor(block, key)
        out.append(block)
    return "".join(out)


def dcbc(data, key):
    blocksize = len(key)
    out = []
    blocks = list(split(data, blocksize))
    for i, block in enumerate(blocks[1:]):
        block = xor(block, key)
        block = xor(block, blocks[i])
        out.append(block)
    return "".join(out)



text = open('plaintext').read()
key = 'kop\\deft(olgqa]x'
ctext = cbc(text, key)
print ctext

print
print dcbc(ctext, key)

#open('ciphertext2', 'wb').write(ctext)
