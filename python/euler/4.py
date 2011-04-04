



def main():
    ns = []
    for x in reversed(range(100, 1000)):
        for y in reversed(range(100, 1000)):
            z = x * y

            if str(z) == str(z)[::-1]:
                ns.append(z)
                print z

    ns.sort()
    print ns[-1]
                

main()
