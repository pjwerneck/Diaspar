#!/usr/bin/env python
# encoding: utf-8


import opcode
import types
import dis

locals().update(opcode.opmap)


def findNestedFuncs(fcode):
    # We use this function to recursively search for nested functions
    for const in fcode.co_consts:
        # funções
        if isinstance(const, types.CodeType):
            yield const
            for code in findNestedFuncs(const):
                yield code


def noself(func, inst):
    # A maior parte da mágica está aqui nesta função..

    # Ela receberá a função que define o método a ser
    # modificado e a instância que deve aparecer lá dentro como 'self'
    
    # o que ela faz é simplesmente colocar no início do método o
    # equivalente à linha: self = inst

    # primeiro, precisamos do bytecode da função
    code = func.func_code

    # agora precisamos dar uma estripada no objeto código e retirar
    # todos os atributos para recriá-lo mais tarde... nem tudo aqui
    # será alterado, mas tirando tudo facilita depois

    argcount = code.co_argcount       # número de parâmetros
    nlocals = code.co_nlocals         # número de variáveis locais
    stacksize = code.co_stacksize     # tamanho máximo da pilha
    flags = code.co_flags             # algumas flags para o interpretador
    codestring = code.co_code         # o código
    constants = code.co_consts        # as constantes na função. 
    names = code.co_names             # nomes de globais usadas
    varnames = code.co_varnames       # nomes de variáveis usadas
    filename = code.co_filename       # nome do arquivo
    name = code.co_name               # nome da função
    firstlineno = code.co_firstlineno # primeira linha da função
    lnotab = code.co_lnotab            
    freevars = code.co_freevars       # variáveis livres
    cellvars = code.co_cellvars       # variáveis usadas em função aninhada

    # temos de descobrir se há qualquer função aninhada dentro de
    # func... para isso verificamos se há qualquer objeto código
    # definido como constante dentro do código da função, em caso
    # positivo, continua a busca recursivamente
    
    # primeiro, colocamos o nome 'self' na lista de nomes de
    # variáveis... colocamos no final para evitar ter de mudar o
    # índice de todas as outras
    varnames += ('self',)

    # depois, fazemos a mesma coisa com a instância na lista de
    # constantes
    constants += (inst,)

    # como acrescentamos uma variável, aumentamos o número de
    # variáveis locais
    nlocals += 1

    # convertemos a string de código para uma lista com o valor
    # numérico de cada byte
    bcode = map(ord, code.co_code)

    # então colocamos no início do código as instruções para fazer
    # a atribuição self=inst
    bcode = [LOAD_CONST,        
             len(constants)-1,  # carrega a instância na pilha
             0,
             STORE_FAST,
             len(varnames)-1,   # atribui a instância a 'self'
             0] + bcode


    # agora vem a parte complicada... infelizmente, quando definimos
    # as chamadas a 'self' no código sem estar definido localmente, o
    # interpretador vai buscá-lo como global, e não vai encontrar o
    # que definimos localmente logo agora... para consertar isso,
    # precisamos encontrar todas os acessos a globais e substituir
    # aqueles que tentam acessar o 'self' como global por um acesso
    # local

    # para facilitar, vamos usar um iterador...
    itercode = iter(enumerate(bcode))
    
    while 1:
        try:
            i, op = itercode.next()
            # se a instrução precisa de argumentos, pode nos
            # interessar ou não, mas de qualquer maneira precisamos
            # pular os bytes dos argumentos para não confundir um
            # valor com instrução...
            if op >= opcode.HAVE_ARGUMENT:
                # os argumentos vem nos dois bytes seguintes... 
                oparg = itercode.next()[1] + itercode.next()[1]*256
                # procuramos por LOAD_GLOBAL
                if op == LOAD_GLOBAL:
                    # o argumento para LOAD_GLOBAL é o índice do nome
                    # da variável em 'names'... se é 'self',
                    # então é o que procuramos!
                    if names[oparg] == 'self':
                        # substituímos a instrução LOAD_GLOBAL por LOAD_FAST
                        bcode[i] = LOAD_FAST
                        # substituímos o argumento para o índice do
                        # nome 'self' na lista 'varnames'
                        bcode[i+1] = len(varnames)-1
                        # a menos que a função tenha mais de 255
                        # variáveis, não teremos problemas aqui e
                        # podemos colocar 0
                        bcode[i+2] = 0

        except StopIteration:
            # saia do loop quando o iterador esgotar...
            break

    # transformamos a lista com o código numérico novamente em string
    codestring = ''.join(map(chr, bcode))

    # recriamos o objeto código com os valores e byte-code novo: muda
    # apenas 'varnames', 'constants', 'nlocals', e o código, claro...
    ncode = types.CodeType(argcount, nlocals, stacksize, flags, codestring,
                           constants, names, varnames, filename, name,
                           firstlineno, lnotab, freevars, cellvars)
    # note que como 'self' vem originalmente como global, o nome vem
    # em 'names', mas não podemos removê-lo para não atrapalhar com os
    # índices de outras variáveis...

    # finalmente, recriamos e retornamos a função, com tudo de antes,
    # mas com o código novo, alterado
    nfunc = types.FunctionType(ncode, func.func_globals, func.func_name,
                               func.func_defaults, func.func_closure)

    return nfunc


# Depois disso tudo, o resto é moleza...

class NoSelfMethod(object):
    # um descriptor que implementa (mais ou menos) o mesmo que os
    # métodos normais (já que a classe MethodType original não permite
    # herança)....
    def __init__(self, func, instance, cls):
        self.im_func = func
        self.im_self = instance
        self.im_class = cls

    def __get__(self, obj, cls):
        return NoSelfMethod(self.im_func, obj, cls)

    def __call__(self, *args, **kwds):
        # com a diferença de que quando é chamado com uma instância,
        # ele usa nossa função nofunc() para criar a nova versão
        # inserindo o 'self' (sim, ele recria a função fazendo aquilo
        # tudo cada vez que o método é chamado!)
        if self.im_self is None:
            return self.im_func(*args, **kwds)
        else:
            func = noself(self.im_func, self.im_self)
            return func(*args, **kwds)


class NoSelfType(type):
    # E finalmente, uma metaclasse que faz com que suas classes usem o
    # nosso método especial 
    def __new__(mcls, name, bases, dic):
        for k, v in dic.items():
            if callable(v):
                dic[k] = NoSelfMethod(v, None, None)

        return type.__new__(NoSelfType, name, bases, dic)
        

def test():

    # Testando ...

    # Uma global só para garantir que elas não foram alteradas...
    bar = 'bar'

    class C(object):
        __metaclass__ = NoSelfType

        def __init__(a, b, c=None):
            print 'Look mom... no self!', self
            # confirmando que o 'self' apareceu aqui
            print 'I am', self, 'they called me with', a, b, c

        def m(obj):
            # confirmando que o 'self' que aparece aqui e o objeto
            # criado são de fato os mesmos
            assert obj is self
            # confirmando que a global está ok
            assert bar == 'bar'

            def f():
                # FIXME: infelizmente, funções aninhadas usam a
                # instrução LOAD_DEREF para encontrar variáveis do
                # escopo anterior, que aparecem naquela lista
                # 'cellvars' lá em cima, então esta função f() não vai
                # encontrar o 'self' pois tenta procurá-lo como
                # global, o que significa que teremos de fazer outra
                # alteração aqui também, bem mais complicada... por
                # via das dúvidas, vamos testar e conferir que dá
                # erro em todas as implementações e versões...
                try:
                    assert obj is self
                    raise AssertionError('self found from nested function?')
                except NameError:
                    pass
            f()

            # É isso aí... 

    o = C(1, 2, c='foo')
    o.m(o)
        
        
if __name__ == '__main__':
    test()





