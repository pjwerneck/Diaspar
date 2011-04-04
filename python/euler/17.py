

uni = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
     'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
     'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']

dec = ['', 'ten', 'twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy',
     'eighty', 'ninety']



def to_ordinal(n):
    if n == 1000:
        return 'one thousand'
    
    t, x = divmod(n, 1000)
    c, x = divmod(x, 100)
    d, u = divmod(x, 10)

    o = []

    if c:
        o.append(uni[c] + ' hundred')
        if d or u:
            o.append('and')
    else:
        o.append('')

    if d > 1:
        o.append(dec[d] + ' ' + uni[u])
    elif d == 1:
        o.append(uni[u + d*10])
    else:
        o.append(uni[u])
        
    
    return ' '.join(o)
        
        

    
all = ''
for x in range(1, 1001):
    all += to_ordinal(x)

raw = all.split()

raw = ''.join(all)

print len(raw)



    
