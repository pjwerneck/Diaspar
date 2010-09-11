#!/usr/local/bin/python2.6
# -*- coding: ISO8859-1 -*-

import random
import re
import copy

### Constantes
# Letras
VOGAIS = 'aeiou'
CONSOANTES = 'bcdfghjklmnpqrstvwxyz'

# Gênero
FEMININO = F = "f" # feminino
MASCULINO = M = "m" # masculino
NEUTRO = N = "n" # neutro
IGENERO = {'n':0, 'm':1, 'f':2}

# Número
SINGULAR = S = "s" # singular
PLURAL = P ="p" # plural
# Grau
DEFINIDO = D = "d" # definido
INDEFINIDO = I = "i" # indefinido

# 0: pronome 'nenhum', substantivo no singular
# 1: artigo no singular, substantivo no singular
# 2: artigo no plural, substantivo no singular
# 3: plural, "vários"/"alguns"
# 4: plural, "muitos"

# artigos e pronomes
ARTIGOS = {M+D:["nenhum", "o", "os", "vários", "muitos"],
           M+I:["nenhum", "um", "uns", "alguns", "muitos"],
           F+D:["nenhuma", "a", "as", "várias", "muitas"],
           F+I:["nenhuma", "uma", "umas", "algumas", "muitas"],
           }

### flexão de plural para adjetivo e substantivo
# FIXME: melhorar isso
def plural_substantivo_adjetivo(palavra):
    # terminação em r, s, z, acrescenta 'es'
    if re.match('.*[rsz]$', palavra):
        return palavra+'es'

    # terminação em x, faz nada
    if re.match('.*x$', palavra):
        return palavra
    
    return palavra + 's'


def genero_adjetivo(palavra, genero):
    # se masculino, provavelmente não precisará fazer nada
    if genero == M:
        if re.match('.*a$', palavra):
            palavra = re.sub('a$', 'o', palavra)
    if genero == F:
        if re.match('.*o$', palavra):
            palavra = re.sub('o$', 'a', palavra)
    
    return palavra
        
### Metaclasse para gerar classes de palavras aleatoriamente

class MetaPalavra(type):
    def __init__(cls, name, bases, dict):
        super(MetaPalavra, cls).__init__(name, bases, dict)

        # cria a lista para armazenar subclasses
        cls.__subcls__ = [cls]

        # acrescenta a classe a todas suas classes pai
        for outra in bases:
            if outra is object:
                continue
            if cls not in outra.__subcls__:
                outra.__subcls__.append(cls)
        
        cls._log = []


class MetaPalavraAleatoria(MetaPalavra):
    
    def escolhe_subclasse(cls):
        # caso não tenha classes base, escolha uma entre as subclasses
        # dela, recursivamente
        cls = random.choice(cls.__subcls__)
        if not hasattr(cls, '_base'):
            cls = cls.escolhe_subclasse()
        return cls
        
    def __call__(cls, *args, **kwds):
        cls = cls.escolhe_subclasse()
        
        if not kwds:
            # garante que o mesmo termo nunca será repetido em seguida
            # quando há mais de uma opção
            if len(cls._base) > 1:
                if not cls._log:
                    x = random.choice(cls._base)
                    cls._log.append(x)
                else:
                    while 1:            
                        x = random.choice(cls._base)
                        if x != cls._log[-1]:
                            cls._log.append(x)
                            break
            else:
                x = random.choice(cls._base)
                if cls._log[-1] != x:
                    cls._log.append(x)
            if isinstance(x, dict):
                kwds.update(dict(zip(cls._keys, (x,))))
            else:
                kwds.update(dict(zip(cls._keys, x)))
                

        return type.__call__(cls, *args, **kwds)



### classe genérica para palavra
class Palavra(object):
    __metaclass__ = MetaPalavra
    def __init__(self, palavra=None, outra=None):
        self.palavra = palavra
        self.outra = outra
        

class PalavraAleatoria(Palavra):
    __metaclass__ = MetaPalavraAleatoria


### classe base para substantivos
class Substantivo(PalavraAleatoria):
    _keys = ('palavra', 'genero')
    def __init__(self, palavra=None, genero=None, numero=1, outra=None):
        super(Substantivo, self).__init__(palavra=palavra, outra=outra)
        self.genero = genero
        self.numero = numero

    def __enter__(self):
        return self

    def __exit(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        todas = []
        todas.append(self.flexao_numero())
        if self.outra is not None:
            todas.append(str(self.outra))
        return ' '.join(todas)

    def __add__(self, outra):
        # 'outra' aqui é provavelmente adjetivo
        outra = copy.copy(outra)
        raiz = atual = copy.deepcopy(self)
        while atual.outra is not None:
            atual = atual.outra

        outra.genero = self.genero
        outra.numero = self.numero
        atual.outra = outra

        return raiz
            
        
    def __mul__(self, numero):
        new = copy.copy(self)
        new.numero = numero
        return new

    def flexao_numero(self):
        if self.numero <= 1:
            return self.palavra
        elif self.numero > 1:
            return plural_substantivo_adjetivo(self.palavra)


### classe base para artigos, artigos não são aleatórios, tem a
### proxima palavra atribuida com a operacao, e comportamento somente
### na impressao
class Artigo(Palavra):
    def __add__(self, outra):
        self.outra = outra
        return self

class ArtigoDefinido(Artigo):
    def __str__(self):
        if self.outra is None:
            return '<ARTIGO DESCONECTADO>'
        artigo = ARTIGOS[self.outra.genero+D][self.outra.numero]
        todas = [artigo]
        todas.append(str(self.outra))
        return ' '.join(todas)

class ArtigoIndefinido(Artigo):
    def __str__(self):
        if self.outra is None:
            return '<ARTIGO DESCONECTADO>'
        artigo = ARTIGOS[self.outra.genero+D][self.outra.numero]
        todas = [artigo]
        todas.append(str(self.outra))
        return ' '.join(todas)

    
### Classe base para adjetivos, têm seus atributos definidos pelo
### substantivo ao fazer a operacao
class Adjetivo(PalavraAleatoria):
    _keys=('palavra',)
    def __init__(self, palavra=None, genero=None, numero=1, outra=None):
        # 'palavra' em adjetivos pode ser um dicionario com as
        # variações
        super(Adjetivo, self).__init__(palavra=palavra, outra=outra)
        self.genero = genero
        self.numero = numero

    def __str__(self):
        todas = []
        todas.append(self.flexao_genero_numero())
        atual = self.outra
        while atual is not None:
            todas.append(str(atual))
            atual = atual.outra
        return '-'.join(todas)

    def __add__(self, outra):
        # caminha recursivamente até encontrar um adjetivo sem outro
        raiz = atual = copy.deepcopy(self)
        outra = copy.copy(outra)
        while atual.outra is not None:
            atual = atual.outra
        atual.outra = outra
        return raiz
            
    def flexao_genero_numero(self):
        return self.flexao_numero(self.flexao_genero())

    def flexao_genero(self):
        # primeiro tenta com neutro:
        try:
            return self.palavra['n']
        except KeyError:
            pass
        # então tenta com o gênero devido
        try:
            return self.palavra[self.genero]
        except KeyError:
            pass
        # e então faz a conversão com o primeiro que encontrar
        return genero_adjetivo(self.palavra.values()[0], self.genero)

    def flexao_numero(self, palavra):
        if self.numero <= 1:
            return palavra
        elif self.numero > 1:
            return plural_substantivo_adjetivo(palavra)

        
        

class AdjetivoNegativo(Adjetivo):
    _base = [{'m':"inapto"},
             {'n':"incapaz"},
             ]

class AdjetivoPolitico(Adjetivo):
    pass

# Adjetivos negativos políticos
class AdjetivoNegativoPolitico(AdjetivoNegativo, AdjetivoPolitico):
    
    _base = [{'n':"sexista"},
             {'n':"colonialista"},
             {'n':"elitista"},
             {'n':"segregacionista"},
             ]



# Substantivos concretos
class SubstantivoConcreto(Substantivo):
    _base = [('porta', F),
             ('fruta', F),
             ('chave', F),
             ('céu', M),
             ('mar', M),
             ('casa', F),
             ('muro', M),
             ('ramo', M),
             ]



class SubstantivoAbstrato(Substantivo):
    _base = [('teoria', F),
             ('discurso', M),
             ('narrativa', F),
             ('idéia', F),
             ]


class ObjetoAbstratoImportante(Substantivo):
    _base = [('cultura', F),
             ('linguagem', F),
             ('arte', F),
             ('realidade', F),
             ('verdade', F),
             ('sexualidade', F),
             ]


class Ideologia(Substantivo):
    _base = [('capitalismo', M),
             ('Marxismo', M),
             ('socialismo', M),
             ('feminismo', M),
             ('nacionalismo', M),
             ('niilismo', M),
             ]


class MetaExpressao(type):
    def __init__(cls, name, bases, dict):
        super(MetaExpressao, cls).__init__(name, bases, dict)
        cls._log = []

    def __iter__(cls):
        for name, obj in cls.__dict__.items():
            if not name.startswith('expr'):
                continue
            yield obj
        
    def __call__(cls, *args, **kwds):
        metodos = list(cls)
        inst = type.__call__(cls)
        return random.choice(metodos)(inst)


class Expressao(object):
    __metaclass__ = MetaExpressao
    def fexpr1(self):
        "*substantivo-abstrato* *adjetivo*"
        return SubstantivoAbstrato() + Adjetivo()

    def fexpr2(self):
        "*substantivo-abstrato* *adjetivo*"
        return SubstantivoAbstrato() + Adjetivo()

    def expr3(self):
        "*substantivo-abstrato* *adjetivo*"
        sub = SubstantivoAbstrato(palavra='teoria', genero=F)
        return ArtigoDefinido() + (sub*2 + Adjetivo() + Adjetivo() + Adjetivo())



def test():
    print Substantivo() + Adjetivo()
    for x in range(5):
        for y in range(5):
            print ArtigoDefinido() + (Substantivo()*x + Adjetivo())


    print Expressao()

if __name__ == '__main__':
    test()
