#!/usr/bin/env python


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

def FF(a, b, c, d, x, s, ac):
    a += F(b, c, d)
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


def GG(a, b, c, d, x, s, ac):
    a += G(b, c, d)
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


def HH(a, b, c, d, x, s, ac):
    a += H(b, c, d)
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


def II(a, b, c, d, x, s, ac):
    a += I(b, c, d)
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


# the routine MD5Init initializes the message-digest context
# mdContext. All fields are set to zero.

class MD5(object):

    def __init__(self, data):
        
        # Initial 128 bit message digest (4 times 32 bit).
        self.buf = [0, 0, 0, 0]
        
        # Initial message length in bits(!).
        self.length = 0L
        self.count = [0, 0]

        # Initial empty message as a sequence of bytes (8 bit characters).
        self.input = []

        # Length of the final hash (in bytes).
        self.HASH_LENGTH = 16
         
        # Length of a block (the number of bytes hashed in every transform).
        self.DATA_LENGTH = 64

        # Call a separate init function, that can be used repeatedly
        # to start from scratch on the same object.
        self.length = 0L
        self.input = []

        # Load magic initialization constants.
        self.buf = [0x67452301L,
                    0xefcdab89L,
                    0x98badcfeL,
                    0x10325476L,
                    ]


        self.update(data)
        
        

    def _transform(self, inp):

        a, b, c, d = self.buf

        # round 1
        
        S11, S12, S13, S14 = 7, 12, 17, 22        
        
        a = FF(a, b, c, d, inp[ 0], S11, 0xD76AA478L)
        d = FF(d, a, b, c, inp[ 1], S12, 0xE8C7B756L)
        c = FF(c, d, a, b, inp[ 2], S13, 0x242070DBL)
        b = FF(b, c, d, a, inp[ 3], S14, 0xC1BDCEEEL)
        a = FF(a, b, c, d, inp[ 4], S11, 0xF57C0FAFL)
        d = FF(d, a, b, c, inp[ 5], S12, 0x4787C62AL)
        c = FF(c, d, a, b, inp[ 6], S13, 0xA8304613L)
        b = FF(b, c, d, a, inp[ 7], S14, 0xFD469501L)
        a = FF(a, b, c, d, inp[ 8], S11, 0x698098D8L)
        d = FF(d, a, b, c, inp[ 9], S12, 0x8B44F7AFL) 
        c = FF(c, d, a, b, inp[10], S13, 0xFFFF5BB1L) 
        b = FF(b, c, d, a, inp[11], S14, 0x895CD7BEL) 
        a = FF(a, b, c, d, inp[12], S11, 0x6B901122L) 
        d = FF(d, a, b, c, inp[13], S12, 0xFD987193L) 
        c = FF(c, d, a, b, inp[14], S13, 0xA679438EL) 
        b = FF(b, c, d, a, inp[15], S14, 0x49B40821L) 

        # round 2

        S21, S22, S23, S24 = 5, 9, 14, 20

        a = GG(a, b, c, d, inp[ 1], S21, 0xF61E2562L) 
        d = GG(d, a, b, c, inp[ 6], S22, 0xC040B340L) 
        c = GG(c, d, a, b, inp[11], S23, 0x265E5A51L) 
        b = GG(b, c, d, a, inp[ 0], S24, 0xE9B6C7AAL) 
        a = GG(a, b, c, d, inp[ 5], S21, 0xD62F105DL) 
        d = GG(d, a, b, c, inp[10], S22, 0x02441453L) 
        c = GG(c, d, a, b, inp[15], S23, 0xD8A1E681L) 
        b = GG(b, c, d, a, inp[ 4], S24, 0xE7D3FBC8L) 
        a = GG(a, b, c, d, inp[ 9], S21, 0x21E1CDE6L) 
        d = GG(d, a, b, c, inp[14], S22, 0xC33707D6L) 
        c = GG(c, d, a, b, inp[ 3], S23, 0xF4D50D87L) 
        b = GG(b, c, d, a, inp[ 8], S24, 0x455A14EDL) 
        a = GG(a, b, c, d, inp[13], S21, 0xA9E3E905L) 
        d = GG(d, a, b, c, inp[ 2], S22, 0xFCEFA3F8L) 
        c = GG(c, d, a, b, inp[ 7], S23, 0x676F02D9L) 
        b = GG(b, c, d, a, inp[12], S24, 0x8D2A4C8AL) 

        # round 3

        S31, S32, S33, S34 = 4, 11, 16, 23
        
        a = HH(a, b, c, d, inp[ 5], S31, 0xFFFA3942L) 
        d = HH(d, a, b, c, inp[ 8], S32, 0x8771F681L) 
        c = HH(c, d, a, b, inp[11], S33, 0x6D9D6122L) 
        b = HH(b, c, d, a, inp[14], S34, 0xFDE5380CL) 
        a = HH(a, b, c, d, inp[ 1], S31, 0xA4BEEA44L) 
        d = HH(d, a, b, c, inp[ 4], S32, 0x4BDECFA9L) 
        c = HH(c, d, a, b, inp[ 7], S33, 0xF6BB4B60L) 
        b = HH(b, c, d, a, inp[10], S34, 0xBEBFBC70L) 
        a = HH(a, b, c, d, inp[13], S31, 0x289B7EC6L) 
        d = HH(d, a, b, c, inp[ 0], S32, 0xEAA127FAL) 
        c = HH(c, d, a, b, inp[ 3], S33, 0xD4EF3085L) 
        b = HH(b, c, d, a, inp[ 6], S34, 0x04881D05L) 
        a = HH(a, b, c, d, inp[ 9], S31, 0xD9D4D039L) 
        d = HH(d, a, b, c, inp[12], S32, 0xE6DB99E5L) 
        c = HH(c, d, a, b, inp[15], S33, 0x1FA27CF8L) 
        b = HH(b, c, d, a, inp[ 2], S34, 0xC4AC5665L) 

        # round 4

        S41, S42, S43, S44 = 6, 10, 15, 21

        a = II(a, b, c, d, inp[ 0], S41, 0xF4292244L) 
        d = II(d, a, b, c, inp[ 7], S42, 0x432AFF97L) 
        c = II(c, d, a, b, inp[14], S43, 0xAB9423A7L) 
        b = II(b, c, d, a, inp[ 5], S44, 0xFC93A039L) 
        a = II(a, b, c, d, inp[12], S41, 0x655B59C3L) 
        d = II(d, a, b, c, inp[ 3], S42, 0x8F0CCC92L) 
        c = II(c, d, a, b, inp[10], S43, 0xFFEFF47DL) 
        b = II(b, c, d, a, inp[ 1], S44, 0x85845DD1L) 
        a = II(a, b, c, d, inp[ 8], S41, 0x6FA87E4FL) 
        d = II(d, a, b, c, inp[15], S42, 0xFE2CE6E0L) 
        c = II(c, d, a, b, inp[ 6], S43, 0xA3014314L) 
        b = II(b, c, d, a, inp[13], S44, 0x4E0811A1L) 
        a = II(a, b, c, d, inp[ 4], S41, 0xF7537E82L) 
        d = II(d, a, b, c, inp[11], S42, 0xBD3AF235L) 
        c = II(c, d, a, b, inp[ 2], S43, 0x2AD7D2BBL) 
        b = II(b, c, d, a, inp[ 9], S44, 0xEB86D391L) 


        self.buf[0] = (self.buf[0] + a) & 0xffffffffL
        self.buf[1] = (self.buf[1] + b) & 0xffffffffL
        self.buf[2] = (self.buf[2] + c) & 0xffffffffL
        self.buf[3] = (self.buf[3] + d) & 0xffffffffL

        

    def update(self, inBuf):
        # digest

        leninBuf = long(len(inBuf))


        # Compute number of bytes mod 64.
        index = (self.count[0] >> 3) & 0x3FL

        # Update number of bits.
        self.count[0] = self.count[0] + (leninBuf << 3)
        if self.count[0] < (leninBuf << 3):
            self.count[1] = self.count[1] + 1
        self.count[1] = self.count[1] + (leninBuf >> 29)

        partLen = 64 - index

        if leninBuf >= partLen:
            self.input[index:] = map(None, inBuf[:partLen])
            self._transform(_longfy(self.input))
            i = partLen
            while i + 63 < leninBuf:
                self._transform(_longfy(map(None, inBuf[i:i+64])))
                i = i + 64
            else:
                self.input = map(None, inBuf[i:leninBuf])
        else:
            i = 0
            self.input = self.input + map(None, inBuf)


    def digest(self):
        """Terminate the message-digest computation and return digest.

        Return the digest of the strings passed to the update()
        method so far. This is a 16-byte string which may contain
        non-ASCII characters, including null bytes.
        """

        input = [] + self.input
        count = [] + self.count

        index = (self.count[0] >> 3) & 0x3fL

        if index < 56:
            padLen = 56 - index
        else:
            padLen = 120 - index

        padding = ['\200'] + ['\000'] * 63
        self.update(padding[:padLen])

        # Append length (before padding).
        bits = _longfy(self.input[:56]) + count


        self._transform(bits)

        # Store state in digest.
        print self.buf
        
        digest = _bytefy(self.buf)

        self.input = input 
        self.count = count 

        return digest


    def hexdigest(self):
        """Terminate and return digest in HEX form.

        Like digest() except the digest is returned as a string of
        length 32, containing only hexadecimal digits. This may be
        used to exchange the value safely in email or other non-
        binary environments.
        """

        d = map(None, self.digest())
        d = map(ord, d)
        d = map(lambda x:"%02x" % x, d)
        d = ''.join(d)

        return d



def md5(arg=None):
    """Return a new md5 object.

    If arg is present, the method call update(arg) is made.
    """

    md5 = MD5()
    if arg:
        md5.update(arg)

    return md5


def test():
    #s = "Oh no I said too much. I haven't said enough."
    s = open('../resultado_exame.pdf').read()

    a = MD5(s).hexdigest()

    import hashlib

    b = hashlib.md5(s).hexdigest()

    print a
    print b
    assert a == b


if __name__ == '__main__':
    test()
