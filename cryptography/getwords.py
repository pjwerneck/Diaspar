


data = open('words').readlines()


words = []
for line in data:
    if not line.strip():
        continue
    i1, w1, i2, w2 = line.split()
    words.append((int(i1), w1))
    words.append((int(i2), w2))


words.sort(key=lambda c: c[0])

i, words = zip(*words)
for word in words:
    print word
    
