
# coding: UTF-8

import itertools
import sys
import random
from pprint import pprint


WORDS = [line.strip() for line in open('commonwords')]



def f(text, key):
    # Esta é a função de encriptação, faz o xor com cada byte
    for a, b in zip(text, itertools.cycle(key)):
        yield chr(ord(a) ^ ord(b))


def split_blocks(data, size):
    # esta função apenas divide o texto em blocos do tamanho da chave
    n = len(data)
    for i, j in zip(xrange(0, n, size), xrange(size, n+1, size)):
        yield ''.join(data[i:j])


def find_keysize(ctext, rounds=50, thres=0.05):
    # Esta é a função que encontra o tamanho da chave através do
    # índice de coinciências. rounds é o número máximo de shifts
    # feitos, inicialmente 50. thres é o valor que a função usa para
    # nivelar as coincidências e encontrar a chave pelos múltiplos,
    # inicialmente 6%, para inglês.

    # A função vai ajustar dinamicamente esses valores até encontrar,
    # chamando recursivamente, mas ela não foi muito bem testada,
    # então se ficar muito tempo aqui e pela saída não houver pista
    # nenhuma, é melhor verificar o funcionamento.   

    # armazena os valores encontrados
    d = []

    # quando o threshold cair abaixo desse valor, dobra o número de
    # rounds e reseta o threshold em 6%
    #if thres <= 0.04:
    #    return find_keysize(ctext, rounds*2, thres=0.06)
        
    # aqui é o trabalho de verdade... faz shift, conta as
    # coincidências acima do threshold e armazena na lista
    for shift in xrange(1, rounds):
        a = ctext
        b = ' '*shift + a
        n = sum(x==y for x, y in zip(a, b))

        #if float(n)/len(a) > thres:
        print 'shift %d bytes, %d out of %d, %f'%(shift, n, len(a), float(n)/len(a))
        #d.append(shift)
        continue
    print
    return
    # se encontramos poucos valores, diminui o threshold, em 0.1%
    if len(d) < 5:
        return find_keysize(ctext, rounds, thres-0.001)

    # encontrou valores o suficiente para tentar algo
    print "current: ", d, thres, rounds

    matches = 0
    for i, low in enumerate(d):
        for j, high in enumerate(d[i:]):
            if high % low:
                if matches > 0:
                    # apareceu um não múltiplo quando já havia
                    # coincidências. aumenta o threshold
                    return find_keysize(ctext, rounds, thres+0.001)
                else:
                    # diminui o threshold
                    return find_keysize(ctext, rounds, thres-0.001)
            else:
                # encontrou um múltiplo, incrementa o contador
                matches += 1
        else:
            # saiu do loop naturalmente...
            if matches < 4:
                # poucos múltiplos encontrados, diminui o threshold
                return find_keysize(ctext, rounds, thres-0.001)
            else:
                # 4 ou mais múltiplos encontrados. já é um bom chute
                # para o tamanho da chave!
                return low
    else:
        # saiu do loop naturalmente, não encontrou nada... diminui o
        # threshold
        return find_keysize(ctext, rounds, thres-0.001)


def asc2hex(data):
    # converte de ASCII para hexadecimal, para facilitar a visualização
    return ''.join('%02x'%ord(c) for c in data)


def joincount(src, dest):
    # faz um update dos dicionários de contagem de caracteres
    for i, d in enumerate(src):
        for k, v in d.items():
            if k not in dest[i]:
                dest[i][k] = v
            else:
                dest[i][k] += v


def wordfill(word, n):
    # gera um bloco com a palavra repetida criando um bloco de tamanho
    # n, e ajustada para cada offset possível, ou seja:
    #
    # wordfill('the', 10)
    #      ...
    #     'thethethet'
    #     'hethetheth'
    #     'ethethethe'
    
    offsets = [word[i:]+word[:i] for i in range(len(word))]
    
    for word in offsets:
        final = word
    
        while len(final) < n:
            final += word
        final = final[:n]
        yield final


def wordgen(wordsdb, n):
    # gera os blocos de palavras a partir da lista
    for i, word in enumerate(wordsdb):
        print '%dth word: %s'%(i+1, word)
        w = len(word)
        # criamos varias combinacoes para cada palavra
        cases = []

        # primeiro, plana..
        cases.append(word)
        # com primeira letra maiuscula
        cases.append(word.capitalize())
        # toda em maiusculas
        cases.append(word.upper())
        
        for case in cases:
            # plana
            for v in wordfill(case, n):
                yield v
            # com espaço à direita
            for v in wordfill(case + ' ', n):
                yield v


def word_attack(data):
    # faz o ataque de fato
    n = len(data[0])
    words = wordgen(WORDS, n)
    
    # armazena a contagem de ocorrência dos caracteres para cada
    # coluna da chave
    charcount = [{} for x in range(n)]

    for word in words:
        # juntamos texto cifrado e bloco da palavra com o algoritmo
        mixed = [''.join(f(block, word)) for block in data]
        # transpôe para colunas
        columns = map(list, zip(*mixed))

        # armazena a contagem temporária
        tmpcount = [{} for x in range(n)]

        # conta a ocorrência de cada caracter em cada coluna
        for i, column in enumerate(columns):        
            for char in column:
                if char in tmpcount[i]:
                    continue
                c = column.count(char)
                if c > 1:
                    tmpcount[i][char] = c

        # atualiza a contagem global com a temporária
        joincount(tmpcount, charcount)
        #print word
        #print guesskey(charcount)
        #print

    return charcount


def guesskey(keydata):
    # tenta adivinhar a chave a partir das estatísticas no dicionário
    # que conta a ocorrência de caracteres

    # no momento implementa só o óbvio: o caracter que aparece mais.
    testkey = [' '] * len(keydata)
    for i, d in enumerate(keydata):
        d = d.items()
        d.sort(key=lambda v: v[1])
        testkey[i] = d[-1][0]

    return ''.join(testkey)

                

def main():

    # o texto encriptado
    ctext = open('ciphertext').read()

    #sp =list(split_blocks(asc2hex(ctext), 8))

    #for i, j in zip(xrange(0, len(sp), 4), xrange(4, len(sp)+1, 4)):
    #    print ' '.join(sp[i:j])
    
    #return


    # tenta encontrar o tamanho da chave
    keysize = find_keysize(ctext)
    return
    keysize = 16

    if keysize is None:
        raise ValueError('no guess for keysize')
    else:
        print "I think keysize is:", keysize

    # divide o texto em blocos do tamanho da chave
    blocks = list(split_blocks(ctext, keysize))
  
    #pprint(map(asc2hex, blocks))

    # Faz o ataque com as 500 palavras mais comuns. Em inglês cada
    # byte contém apenas 1.3 bits de informação real, o que significa
    # que se acertamos apenas 16% das palavras existentes no texto, já
    # teremos redundância o suficiente para adivinhar a chave
    keydata = word_attack(blocks)
    
    guess = guesskey(keydata)

    print "I guess the key is:", repr(guess)

    print "Trying to decript the text:"

    print '-'*50
    print ''.join(f(ctext, guess))
    print '-'*50

    print
    print 'Was it a good guess?'
                  


def break_file_sip():
    data = open('file.sip').read()[:5000]
    keysize = find_keysize(data, 1000)
    print keysize

    
if __name__ == '__main__':
    #main()
    break_file_sip()
