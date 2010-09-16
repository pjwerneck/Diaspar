
from __future__ import division

#start at 3cm
table = [1023,
         850,
         780,
         670,
         600,
         530,
         473,
         433,#10
         394,
         361,
         335,
         311,
         298,
         278,
         258,
         245,
         238,
         223,#20
         209,
         203,
         189,
         182,
         176,
         169,
         162,
         154,
         148,
         142,#30
         136,
         128,
         122,
         118,
         116,
         112,
         110,
         104,
         102,
         96,#40
         90,
         88]



dict_table = {}

for i, v in enumerate(table):
    dict_table[v] = i+3

#print dict_table


def build_table():
    out_table = []
    v = 100
    lasti = 0
    for i in range(1024):
        try:
            v = dict_table[i]
            lasti = i
            w = v
        except KeyError:
            # find next
            for j in range(i, 1024):
                if j in dict_table:
                    break
#            print v, lasti, i, j, dict_table[j]
#            print "interval", (j-lasti)
#            print "factor", i-lasti
            w = v - (i-lasti)/(j-lasti)
#            print w
        out_table.append(int(round(w, 1)*10))
    assert len(out_table) == 1024

    print "const int RANGE_TABLE[] = {"
    print ",".join(map(str, out_table))
    print "}"
    

build_table()
