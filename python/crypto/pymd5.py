#!/usr/bin/env python


# some functions to help bitwise transform

def _bytefy(longs):
    # convert a list of 32 bit long to a string
    chars = []
    for n in longs:
        bytes = [(n & 0x000000ff) >> 0,             
                 (n & 0x0000ff00) >> 8,             
                 (n & 0x00ff0000) >> 16,             
                 (n & 0xff000000) >> 24,
                 ]
        chars.extend(bytes)
        
    return ''.join(map(chr, chars))


def _longfy(bytes):
    # convert a string into a list of 32 bit longs
    words = [bytes[i:i+4] for i in range(0, len(bytes), 4)]
    longs = []
    
    for w in words:
        b = map(ord, w)
        n = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
        longs.append(n)

    return longs



### md5 implementation

PADDING = [chr(0x80)] + [chr(0x00)]*63


# F, G, H and I are basic MD5 functions

def F(x, y, z):
    return (((x) & (y)) | ((~x) & (z)))

def G(x, y, z):
    return (((x) & (z)) | ((y) & (~z)))

def H(x, y, z):
    return ((x) ^ (y) ^ (z))

def I(x, y, z):
    return ((y) ^((x) | (~z)))

# ROTATE_LEFT rotates x left n bits
def ROTATE_LEFT(x, n):
    return (((x) << (n)) | ((x) >> (32-(n))))
 
# FF, GG, HH, and II transformations for rounds 1, 2, 3, and 4

# Rotation is separate from addition to prevent recomputation

def XX(X, a, b, c, d, x, s, ac):
    a += X(b, c, d)
    a &= 0xffffffff

    a += x
    a &= 0xffffffff

    a += ac
    a &= 0xffffffff

    a = ROTATE_LEFT(a, s)
    a &= 0xffffffff

    a += b
    a &= 0xffffffff
    return a    

def FF(a, b, c, d, x, s, ac):
    return XX(F, a, b, c, d, x, s, ac)

def GG(a, b, c, d, x, s, ac):
    return XX(G, a, b, c, d, x, s, ac)

def HH(a, b, c, d, x, s, ac):
    return XX(H, a, b, c, d, x, s, ac)

def II(a, b, c, d, x, s, ac):
    return XX(I, a, b, c, d, x, s, ac)



class md5(object):
    def __init__(self):
        self.count = [0, 0]

        # load magic initialization constants.
        self.buf = [0x67452301L,
                    0xefcdab89L,
                    0x98badcfeL,
                    0x10325476L,
                    ]

        self.in_data = []
        
    def update(self, data):
        in_buf = data
        in_len = len(data)

        # compute number of bytes mod 64
        mdi = (self.count[0] >> 3) & 0x3F

        # update number of bits
        if self.count[0] + (in_len << 3) < self.count[0]:
            self.count[1] += 1

        self.count[0] += (in_len << 3)
        self.count[1] += (in_len >> 29)

        part_len = 64 - mdi

        # transform as many times as possible
        if in_len >= part_len:
            self.in_data[mdi:] = in_buf[:part_len]
            self.transform(_longfy(self.in_data))

            i = part_len
            while i + 63 < in_len:
                self.transform(_longfy(in_buf[i:i+64]))
                i = i+64
            else:
                self.in_data = list(in_buf[i:in_len])
        else:
            self.in_data.extend(list(in_buf))


    def digest(self):        
        # save number of bits and data
        count = self.count[:]
        in_data = self.in_data[:]
        buf = self.buf[:]
        
        # compute number of bytes mod 64
        mdi = (self.count[0] >> 3) & 0x3F

        # pad out to 56 mod 64
        if mdi < 56:            
            pad_len = 56 - mdi
        else:
            pad_len = 120 - mdi

        self.update(PADDING[:pad_len])

        # append length in bits and transform
        bits = _longfy(self.in_data[:56]) + count

        self.transform(bits)

        digest = _bytefy(self.buf)

        # copy number of bits and data back
        self.count = count 
        self.in_data = in_data
        self.buf = buf

        return digest


    def hexdigest(self):
        d = ''.join(['%02x'%ord(x) for x in self.digest()])
        return d

            
    def transform(self, x):

        a, b, c, d = self.buf

        # round 1
        
        S11, S12, S13, S14 = 7, 12, 17, 22        
        
        a = FF(a, b, c, d, x[ 0], S11, 0xD76AA478)
        d = FF(d, a, b, c, x[ 1], S12, 0xE8C7B756)
        c = FF(c, d, a, b, x[ 2], S13, 0x242070DB)
        b = FF(b, c, d, a, x[ 3], S14, 0xC1BDCEEE)
        a = FF(a, b, c, d, x[ 4], S11, 0xF57C0FAF)
        d = FF(d, a, b, c, x[ 5], S12, 0x4787C62A)
        c = FF(c, d, a, b, x[ 6], S13, 0xA8304613)
        b = FF(b, c, d, a, x[ 7], S14, 0xFD469501)
        a = FF(a, b, c, d, x[ 8], S11, 0x698098D8)
        d = FF(d, a, b, c, x[ 9], S12, 0x8B44F7AF) 
        c = FF(c, d, a, b, x[10], S13, 0xFFFF5BB1) 
        b = FF(b, c, d, a, x[11], S14, 0x895CD7BE) 
        a = FF(a, b, c, d, x[12], S11, 0x6B901122) 
        d = FF(d, a, b, c, x[13], S12, 0xFD987193) 
        c = FF(c, d, a, b, x[14], S13, 0xA679438E) 
        b = FF(b, c, d, a, x[15], S14, 0x49B40821) 

        # round 2

        S21, S22, S23, S24 = 5, 9, 14, 20

        a = GG(a, b, c, d, x[ 1], S21, 0xF61E2562) 
        d = GG(d, a, b, c, x[ 6], S22, 0xC040B340) 
        c = GG(c, d, a, b, x[11], S23, 0x265E5A51) 
        b = GG(b, c, d, a, x[ 0], S24, 0xE9B6C7AA) 
        a = GG(a, b, c, d, x[ 5], S21, 0xD62F105D) 
        d = GG(d, a, b, c, x[10], S22, 0x02441453) 
        c = GG(c, d, a, b, x[15], S23, 0xD8A1E681) 
        b = GG(b, c, d, a, x[ 4], S24, 0xE7D3FBC8) 
        a = GG(a, b, c, d, x[ 9], S21, 0x21E1CDE6) 
        d = GG(d, a, b, c, x[14], S22, 0xC33707D6) 
        c = GG(c, d, a, b, x[ 3], S23, 0xF4D50D87) 
        b = GG(b, c, d, a, x[ 8], S24, 0x455A14ED) 
        a = GG(a, b, c, d, x[13], S21, 0xA9E3E905) 
        d = GG(d, a, b, c, x[ 2], S22, 0xFCEFA3F8) 
        c = GG(c, d, a, b, x[ 7], S23, 0x676F02D9) 
        b = GG(b, c, d, a, x[12], S24, 0x8D2A4C8A) 

        # round 3

        S31, S32, S33, S34 = 4, 11, 16, 23
        
        a = HH(a, b, c, d, x[ 5], S31, 0xFFFA3942) 
        d = HH(d, a, b, c, x[ 8], S32, 0x8771F681) 
        c = HH(c, d, a, b, x[11], S33, 0x6D9D6122) 
        b = HH(b, c, d, a, x[14], S34, 0xFDE5380C) 
        a = HH(a, b, c, d, x[ 1], S31, 0xA4BEEA44) 
        d = HH(d, a, b, c, x[ 4], S32, 0x4BDECFA9) 
        c = HH(c, d, a, b, x[ 7], S33, 0xF6BB4B60) 
        b = HH(b, c, d, a, x[10], S34, 0xBEBFBC70) 
        a = HH(a, b, c, d, x[13], S31, 0x289B7EC6) 
        d = HH(d, a, b, c, x[ 0], S32, 0xEAA127FA) 
        c = HH(c, d, a, b, x[ 3], S33, 0xD4EF3085) 
        b = HH(b, c, d, a, x[ 6], S34, 0x04881D05) 
        a = HH(a, b, c, d, x[ 9], S31, 0xD9D4D039) 
        d = HH(d, a, b, c, x[12], S32, 0xE6DB99E5) 
        c = HH(c, d, a, b, x[15], S33, 0x1FA27CF8) 
        b = HH(b, c, d, a, x[ 2], S34, 0xC4AC5665) 

        # round 4

        S41, S42, S43, S44 = 6, 10, 15, 21

        a = II(a, b, c, d, x[ 0], S41, 0xF4292244) 
        d = II(d, a, b, c, x[ 7], S42, 0x432AFF97) 
        c = II(c, d, a, b, x[14], S43, 0xAB9423A7) 
        b = II(b, c, d, a, x[ 5], S44, 0xFC93A039) 
        a = II(a, b, c, d, x[12], S41, 0x655B59C3) 
        d = II(d, a, b, c, x[ 3], S42, 0x8F0CCC92) 
        c = II(c, d, a, b, x[10], S43, 0xFFEFF47D) 
        b = II(b, c, d, a, x[ 1], S44, 0x85845DD1) 
        a = II(a, b, c, d, x[ 8], S41, 0x6FA87E4F) 
        d = II(d, a, b, c, x[15], S42, 0xFE2CE6E0) 
        c = II(c, d, a, b, x[ 6], S43, 0xA3014314) 
        b = II(b, c, d, a, x[13], S44, 0x4E0811A1) 
        a = II(a, b, c, d, x[ 4], S41, 0xF7537E82) 
        d = II(d, a, b, c, x[11], S42, 0xBD3AF235) 
        c = II(c, d, a, b, x[ 2], S43, 0x2AD7D2BB) 
        b = II(b, c, d, a, x[ 9], S44, 0xEB86D391) 

        self.buf[0] = (self.buf[0] + a) & 0xffffffff
        self.buf[1] = (self.buf[1] + b) & 0xffffffff
        self.buf[2] = (self.buf[2] + c) & 0xffffffff
        self.buf[3] = (self.buf[3] + d) & 0xffffffff


def test():
    import random
    import hashlib

    x = open('../../misc/goldenratio/tmp.png').read()

    m = md5()
    n = hashlib.md5()

    i = 0

    while i < len(x):
        j = random.randint(i, len(x))
        m.update(x[i:j])
        n.update(x[i:j])

        a = m.hexdigest()
        b = n.hexdigest()
        print a
        print b
        print

        assert a == b

        i = j



if __name__ == '__main__':
    test()
