

import random

key = '28dhnwjwx2'
text = "Why, Lord, do you stand far off? Why do you pay no attention during times of trouble?"

def crypt(text, key):
    random.seed(key)
    for c in text:
        yield chr(ord(c) ^ random.randint(0, 255))


print repr(''.join(crypt(text, key)))


