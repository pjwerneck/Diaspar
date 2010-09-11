
#ifndef HTML
#define TROFF_2COLUMN
#endif



#include <stdmap.pbi>
#include <format.pbi>

// regras iniciam aqui
//teste: teste2* teste2* teste2* teste2* teste2* teste2* teste2* teste2* teste2*;

//teste2: ?sub=novo-termo $artigo " " $sub "\n\n";
//teste2: sentenca3"\n\n";




saida:
       ?v-assunto<<[novo-termo | ideologia | movimento-artistico]
       ?v-artigo<<$artigo
       ?v-assunto2<<[novo-termo | ideologia]
       ?v-artigo2<<$artigo
       ?v-assunto3<<novo-termo
       ?v-artigo3<<$artigo
       ?v-citavel<<artista-citavel

       PROLOGUE TITLE(titulo>upcase-first) autores-formatados 
       BODY secoes EPILOGUE;



titulo: titulo2>upcase-first 
      | titulo-suave ": " titulo2>upcase-first ;

titulo2: $v-assunto " nos trabalhos de " $v-citavel
       | $v-assunto " nos trabalhos de " artista
       | $v-assunto " nos trabalhos de " artista-citavel 
       | p-titulo-dois-termos($v-assunto $v-assunto2)
       | p-titulo-dois-termos($v-assunto $v-assunto2)
       | p-titulo-dois-termos($v-assunto $v-assunto2)
       | p-titulo-tres-termos($v-assunto $v-assunto2 $v-assunto3)
;

rodape-titulo: rodape-titulo2>upcase-first
             | titulo-suave ": " rodape-titulo2>upcase-first
;

rodape-titulo2: termo " nos trabalhos de " $v-citavel
       | termo " nos trabalhos de " artista
       | termo " nos trabalhos de " artista-citavel 
       | termo " nos trabalhos de " artista
       | termo " nos trabalhos de " artista-citavel 

       | $v-assunto " nos trabalhos de " artista
       | $v-assunto2 " nos trabalhos de " artista
       | $v-assunto3 " nos trabalhos de " artista

       | $v-assunto " nos trabalhos de " artista-citavel 
       | $v-assunto2 " nos trabalhos de " artista-citavel 
       | $v-assunto3 " nos trabalhos de " artista-citavel 

       | p-titulo-dois-termos(termo termo)
       | p-titulo-dois-termos(termo termo)
       | p-titulo-dois-termos(termo termo)
       | p-titulo-dois-termos(termo termo)
       | p-titulo-dois-termos(termo $v-assunto)
       | p-titulo-dois-termos($v-assunto termo)
       | p-titulo-dois-termos(termo $v-assunto2)
       | p-titulo-dois-termos($v-assunto2 termo)
       | p-titulo-dois-termos($v-assunto $v-assunto2)
       | p-titulo-dois-termos($v-assunto2 $v-assunto)

       | p-titulo-tres-termos(termo termo termo)
       | p-titulo-tres-termos(termo termo termo)
       | p-titulo-tres-termos(termo termo $v-assunto)
       | p-titulo-tres-termos(termo termo $v-assunto2)
       | p-titulo-tres-termos(termo termo $v-assunto3)
;


p-titulo-dois-termos(foo bar): foo " e " bar | bar " e " foo;


p-titulo-tres-termos(foo bar baz): foo ", " bar " e " baz
                                 | foo ", " baz " e " bar
                                 | bar ", " foo " e " baz
                                 | bar ", " baz " e " foo
                                 | baz ", " foo " e " bar
                                 | baz ", " bar " e " foo
;


titulo-suave: fazendo-algo-com>upcase-first " " intelectual
            | ?sub=substantivo-abstrato
              ?gen=$artigo>genero-por-artigo
              $sub>pluralizar>upcase-first " " 
              adjetivo($gen)>pluralizar-adjetivo>upcase-first

            | ?sub=substantivo-concreto
              ?gen=$artigo>genero-por-artigo
               $artigo>upcase-first " " $sub>upcase-first " "
               adjetivo-concreto($gen)>upcase-first
           
            | ?sub=algo-de2
              $artigo>upcase-first " " $sub>upcase-first " "
              ?sub=objeto-nebuloso>upcase-first
              $artigo>preposicao-de " " $sub
           
            | ?sub=algo-de2
              $artigo>upcase-first " " $sub>upcase-first " "
              ?sub=objeto-importante>upcase-first
              $artigo>preposicao-de " " $sub

            | ?sub=objeto-nebuloso
              $artigo>upcase-first " " $sub>upcase-first " "
              ?sub=algo-de2>upcase-first
              $artigo>preposicao-de " " $sub

            | ?sub=objeto-nebuloso
              $sub>pluralizar>upcase-first " "
              ?sub=algo-de2>upcase-first
              $artigo>preposicao-de " " $sub

            | ?sub=movimento-artistico>upcase-first
              fazendo-algo-ao-movimento>upcase-first " " $artigo " "
              $sub
;



fazendo-algo-com: "lendo"
                | "desconstruindo"
                | "esquecendo"
;


fazendo-algo-ao-movimento: "reinventando"
                         | "desconstruindo"
                         | "reafirmando"
;


autores-formatados: autores
;

autores: autor-artigo+ | autor-artigo
;

autor-artigo: AUTHOR_INST(nome [departamento ", " instituicao-academica]);

departamento: "Departamento de " topico-departamento;


topico-departamento: "Letras"
                   | "Literatura"
                   | "Ciências Políticas"
                   | "Sociologia"
                   | "Filosofia"
                   | "Filologia"

;

instituicao-academica: "Universidade do Estado " ?sub=estado-brasileiro $prep " " $sub
                     | "Universidade Estadual " ?sub=estado-brasileiro $prep " " $sub
                     | "Universidade de São Paulo"
                     | "Universidade Nove de Julho"
                    // acrescentar mais

;


tipo-de-instituicao: "Universidade " ["Federal" | "Estadual"]
                   | ["Instituto "|"Centro "]"de "["Tecnologia "|"Pesquisa "]
;


estado-brasileiro: "Acre" ?prep="do"
                 | "Alagoas" ?prep="de"
                 | "Amapá" ?prep="de"
                 | "Amazonas" ?prep="do"
                 | "Bahia" ?prep="da"
                 | "Ceará" ?prep="do"
                 | "Distrito Federal" ?prep="do"
                 | "Espírito Santo" ?prep="do"
                 | "Goiás" ?prep="de"
                 | "Maranhão" ?prep="do"
                 | "Mato Grosso" ?prep="do"
                 | "Mato Grosso do Sul" ?prep="do"
                 | "Minas Gerais" ?prep="de"
                 | "Pará" ?prep="do"
                 | "Paraíba" ?prep="da"
                 | "Paraná" ?prep="do"
                 | "Pernambuco" ?prep="de"
                 | "Piauí" ?prep="do"
                 | "Rio de Janeiro" ?prep="do"
                 | "Rio Grande do Norte" ?prep="do"
                 | "Rio Grande do Sul" ?prep="do"
                 | "Rondônia" ?prep="de"
                 | "Roraima" ?prep="de"
                 | "Santa Catarina" ?prep="de"
                 | "São Paulo" ?prep="de"
                 | "Sergipe" ?prep="do"
                 | "Tocantins" ?prep="de"
;




// texto comeca aqui

secoes: secao+ secao+ secao-final;

secao: SECTION(titulo-secao)  PBRK paragrafos;

secao-final: SECTION("Conclusão") PBRK paragrafos-final;

titulo-secao: termo " e " v-assunto3=novo-termo ?v-artigo3=$artigo
            | v-citavel<<artista-citavel " e " termo
            | objeto-nebuloso>pluralizar " " 
              ?sub=algo-de2 $artigo>preposicao-de " " $sub
;


paragrafos: intro-paragrafo PBRK paragrafos2;

paragrafos-final: intro-paragrafo PBRK paragrafo-final;


paragrafos2: paragrafos PBRK paragrafo
           | paragrafos PBRK paragrafo
           | paragrafos PBRK paragrafo
           | paragrafo PBRK paragrafo "\n\n" paragrafo
           | paragrafo PBRK paragrafo
;

paragrafo-final: s-podemos-concluir-que>upcase-first sentenca2 sentenca+
;


intro-paragrafo: intro-sentenca paragrafo;

paragrafo: sentenca+;


intro-sentenca: intro-sentenca2>upcase-first;


intro-sentenca2: 
// Nos trabalhos de *artista*, uma *ideia central* é *conceito predominante
                 "nos trabalhos de " $v-citavel
                 ", "
                 ?sub=s-ideia-central
                 $artigo>indefine-artigo
                 " " $sub " " $conj " " conceito-predominante ". "

               | 

// Se alguém *examina* o *termo central1*, *passa a encarar* uma *escolha*:
// *aceitar/rejeitar* o *termo central2* ou *concluir* que *resultado*.
                 se-quando " alguém " examina " " 
                 ?sub=termo
                 $artigo " " $sub 
                 ", " 
                 ?sub=escolha

                 [ passa-a-encarar2 " " $artigo>indefine-artigo " " $sub": "|
                   passa-a-encarar1 " " $sub " de "]

                 aceitar-ou-rejeitar " " 
                 ?sub=termo 
                 $artigo " " $sub 
                 " ou " s-concluir " que " resultado". "

               | "o tema " s-central " d" obra>remove-espacos-iniciais 
                 " é " descricao-de-conceito ". "

               | intro-sentenca-coisa-estado

;

intro-sentenca-coisa-estado: 
// "A "*coisa* é *estado*", diz *intelectual*; *entretanto* *segundo* *fulano*, não é tanto a *coisa* que é/está *estado*, mas sim *algo* da *coisa*.

        ?coisa=objeto-importante
        ?artigo-coisa=$artigo
        //"\"" $artigo>upcase-first " " $coisa " " 
        ?estado=estado-de-ser        
        ?artigo-estado=$artigo
        //$conj " " $estado "\", diz " intelectual "; " 
        intelectual-diz
        entretanto-forcado>remove-virgula " " segundo " " 

        foo=sobrenome-generico rodape-cita($foo)

        ", não é tanto " $artigo-coisa " " $coisa 
        " que " $conj " " $estado ", " mas-sim " " 
        ?sub=algo-de
        " " $sub " " $artigo-coisa>preposicao-de " " $coisa ". "
;


intelectual-diz: 
        intelectual>upcase-first " diz que " $artigo-coisa " " $coisa " " 
        $conj " " $estado ", "

      | "\"" $artigo-coisa>upcase-first " " $coisa " " $conj " "
        $estado "\", diz " intelectual "; "
;



conceito-predominante: "a distinção entre " foo=dualismo " e " $foo>oposto
                     //FIXME 
;


sentenca: sentenca2>upcase-first 
        | preambulo>upcase-first sentenca2
        | sentenca2>remove-ponto>upcase-first ligacao sentenca2
;

sentenca2 : 
// A *suposicao* *implica que* *resultado*
           ?sub=suposicao $artigo " " $sub " " implica-que resultado ". "

// *Intelectual* *usa* o termo *'termo'* para *denotar* o *conceito.
          | intelectual " " s-usa " o termo '" termo "' para " 
            denotar descricao-de-conceito". "

// *Se x é y*, *temos* *de escolher* entre *o termo1* e *o termo2*.
          | justificador " " temos escolher " entre "
            ?sub=termo
            $artigo " " $sub " e "
            ?sub=termo
            $artigo " " $sub". "

// O tema *central* da *obra* vem a ser *conceito*
          | "o tema " s-central " d" obra>remove-espacos-iniciais 
            [" vem a ser "| " é "]
            descricao-de-conceito". "

// *Intelectual* promove o uso de *termo* para *fazer algo a coisa*
          | intelectual " " promove 
            ?sub=termo
            " o uso " $artigo>preposicao-de " " $sub 
            " para " frase-imperativa ". "

// *Um número de* *coisas abstratas* *envolvendo conceito* existem.
          | ?sub=substantivo-abstrato
            adjetivo-numerico-plural " " $sub>pluralizar " " descricao-abstrata
            " " existe-plural ". "
// sentenca sobre artista
          | sentenca-sobre-artista-citavel($v-citavel)

// O sujeito é *passado* no *objeto* que inclui o *objeto* como *objeto*
          | "o sujeito é " verbo-neutro>verbo-para-passado 
            ?sub=termo 
            //$artigo>indefine-artigo 
            " " $artigo>preposicao-em " "
            " " $sub " que inclui "
            ?sub=objeto-abstrato-importante $artigo " " $sub " como " 
            ?sub=objeto-singular $artigo>indefine-artigo " " $sub ". "

          | ?sub=termo
            p-sentenca-sobre-conceito($artigo $sub)

          | sentenca3
;


sentenca3: 
// Acabaram-se os dias em que um "positivista" era alguém que invoca factos contra o Marxismo.
           acabaram-se " um \"" 
           ista=adjetivo-base2"ista"
           "\" era " 
           ["alguém"|"aquele"] " que " s-afirma 
           [" premissas contra " | " fatos contra "| " "]
           ?sub=[substantivo-abstrato |ideologia]
           $artigo " " $sub ". "

;

acabaram-se: acabou-plural " " ["os"|"aqueles"]" dias " ["em que"|"nos quais"]
           | acabou-singular " " ["o"|"aquele"]" tempo " ["em que"|"no qual"]
           | acabou-singular " " ["a"|"aquela"]" era " ["em que"|"na qual"]
;

acabou-singular: "acabou-se"
               | "encerrou-se"
               | "chegou ao fim"
;

acabou-plural: "acabaram-se"
             | "encerraram-se"
             | "chegaram ao fim"
;


criar-citacao: ".*" -> "$"/"-trabalhos"
;


enviado-sobre-citavel-e-dualismo(artista dualismo):
          "'"@artista>criar-citacao"'" " é sobre " 
          " " dualismo " enquanto "
          "'"@artista>criar-citacao"'" " é sobre " 
          dualismo>oposto
;



sentenca-sobre-artista-citavel(artista):
          parte-de " '" @artista>criar-citacao "' " tambem-evidente-em " '"
          @artista>criar-citacao"'" adverbio-posjustifica ". "

        | enviado-sobre-citavel-e-dualismo(artista dualismo) ". "         

        | "em '" @artista>criar-citacao "', " artista " " diz-algo
          "; em '" @artista>criar-citacao "'" entretanto artista " "
          diz-algo-mais(artista) ". "

        | justificador tipo-de-trabalho artista " " $conj " "
          trabalho-estado-de-ser ". "
;



trabalho-estado-de-ser: "pós-modern"$gen$plural
                      | "modernista"$plural
                      | "um exemplo de " ideologia " " adjetivo-informal
                      | "reminiscente"$plural" de " artista
                      | "fortalecedor"$gen2$plural
;  


parte-de: 
          algo-de " " 
          ?sub=termo 
          $artigo>preposicao-de " "  $sub " " 
          in-termo
;



// work
obra: tipo-de-trabalho foo=sobrenome-generico rodape-cita($foo)" sobre " 
      ?sub=termo
      $artigo " " $sub
    | tipo-de-trabalho $v-citavel
;



// sentenças parametricas, sobre conceitos

//accept-or-reject
aceitar-ou-rejeitar: "aceitar" 
                   | "rejeitar"
                   | "reconhecer"
                   | "desprezar"
;


p-alternativa-abstrata(art-conc conc): 
                              p-alternativa-abstrata2(art-conc conc)
                            | p-alternativa-abstrata2(art-conc conc) 
                              " e consequentemente " aceitar-ou-rejeitar " que " resultado
;

p-alternativa-abstrata2(art-conc conc): aceitar-ou-rejeitar tipo-de-trabalho fonte-de-ideia " sobre " art-conc " " conc

;

tipo-de-trabalho: " o trabalho de " ?conj="é" ?gen="o" ?plural="" ?gen2=""
                | " as idéias de " ?conj="são" ?gen="a" ?plural="s" ?gen2="a"
                | " a obra de " ?conj="é" ?gen="a" ?plural="" ?gen2="a"
;


p-sentenca-sobre-conceito(art-conc conc): ?sub=papel
                                 $artigo " " $sub 
                                 ?opt=escolha
                                 " tem " $artigo>indefine-artigo " " $opt 
                                 a-fazer ": "
                                 p-alternativa-abstrata(art-conc conc)
                                 " ou, alternativamente, "
                                 ?sub=termo
                                 p-alternativa-abstrata($artigo $sub)". "
;


// descricoes de coisas abstratas, como teorias e discursos

// abst-description
descricao-abstrata: p-envolvendo-termo(termo)
                  | p-envolvendo-conceito(descricao-de-conceito)
;

descricao-abstrata-plural: descricao-abstrata
                         | " que inclui "
;



p-envolvendo-termo(conc): "envolvendo " $artigo " " conc
                      | "sobre " $artigo " " conc
;

p-envolvendo-conceito(conc): conc>envolvendo-por-conceito conc>remove-nao-inicial
                         | "envolvendo " conc
                         | conc>sobre-por-conceito conc>remove-nao-inicial
;


// inverte frase iniciada por não para inserir: "não envolvendo bla bla"
sobre-por-conceito: "^não" -> "não sobre"
                    "^.*" -> "sobre "
;

// inverte frase iniciada por não para inserir: "não envolvendo bla bla"
envolvendo-por-conceito: "^não" -> "não envolvendo"
                         "^.*" -> "envolvendo "
;


// term-or-concept-desc
termo-ou-descricao-de-conceito: termo
                              | descricao-de-conceito
;



// imper-vp
frase-imperativa: ?sub=bogeyman verbo-imperativo-negativo " " $artigo " " $sub
                | ?sub=objeto-importante verbo-imperativo " " $artigo " " $sub
;


// imper-*-verb
verbo-imperativo-negativo: "atacar"
                         | "desafiar"
                         | "desconstruir"
                         | "obstaculizar"
;

verbo-imperativo: verbo-imperativo2
                | verbo-imperativo2 " e " verbo-imperativo2
;

verbo-imperativo2: verbo-imperativo-negativo
                 | "re"verbo-imperativo-negativo
;

verbo-imperativo3: verbo-imperativo-negativo
                 | "analisar"
                 | "modificar"
                 | "alocar"
;


// main-theme-of
tema-principal-de: "o tema " s-central " " $artigo>preposicao-de
                 | "tema caracterizante" ?artigo="o"
                 | "a idéia central " $artigo>preposicao-de
;



// justifier
justificador: ?sub=termo
              "se " $artigo " " $sub " é " ["verdadeir"|"valid"]$artigo ", "
            | nome=sobrenome-generico rodape-cita($nome) " " implica-que

;


// concept-desc
descricao-de-conceito: algo-de>remove-virgula
                       ?sub=objeto-importante
                       ?gen=$artigo>genero-por-artigo
                       " " $artigo>preposicao-de " "
                       $sub " " adjetivo($gen)
                     | ?sub=algo-entre
                       $artigo " " $sub " entre "
                       ?sub=objeto-importante
                       $artigo " " $sub " e "
                       ?sub=objeto-importante
                       $artigo " " $sub
                     | ?sub=substantivo-abstrato
                       p1-descricao-de-conceito($sub $artigo)
;
                       

p1-descricao-de-conceito(algo art-algo): "não" de-fato " " art-algo " "
                                         algo ", mas " art-algo " " 
                                         prefixo-modificador algo

                                       | "não " art-algo " " algo per-se
                                         ", mas " art-algo " " 
                                         prefixo-modificador algo

;


diz-algo: ?sub=termo s-afirma-nega " " $artigo " " $sub
;


diz-algo-mais(artista): diz-algo
;


// SINONIMOS

s-capaz: "capaz"
       | "incapaz"
;

op-capaz: "capaz" <-> "incapaz"
;


s-podemos-concluir-que: "podemos concluir que "
                      | "concluimos que "
                      | "finalmente, "
;

s-usa: "usa"
     | "emprega"
     | "adota"
;

s-concluir: "concluir"
          | "chegar à conclusão"
;

s-ideia-central: "idéia "s-central ?artigo="a" ?conj="é"
               | "conceito "s-central ?artigo="o" ?conj="é"
               | "tópico "s-central ?artigo="o" ?conj="é"
;

s-central: "central"
         | "predominante"
         | "delineador"
         | "dominante"
         | "principal"
         | "caracterizador"
;


s-ainda-que: "ainda que"
           | "conquanto"
           | "mesmo que"
;

mas-sim: "mas sim"
       | "e sim"
;
 

segundo: "segundo"
       | "de acordo com"
;


passa-a-encarar1: "passa a encarar " $artigo
               | "vê-se diante " $artigo>preposicao-de
               | "é levado " $artigo>preposicao-a
               | "tem "$artigo
               | "enfrenta "$artigo
;

passa-a-encarar2: "passa a encarar"
                | "vê-se diante de"
                | "é levado a"
                | "tem "
                | "enfrenta "
;


escolha: "escolha" ?artigo="a"
       | "decisão" ?artigo="a"
       | "opção" ?artigo="a"
       | "dilema" ?artigo="o"
;

a-fazer: ""
       | " a enfrentar"
;

examina: "examina"
       | "avalia"
       | "revisa"
;

se-quando: "se"
         | "quando"
;


s-afirma-nega: s-afirma
             | s-nega
;


s-afirma: "afirma"
        | "reitera"
        | "constrói"
        | "examina"
        | "analisa"
        | "invoca"
;

s-nega: "nega"
      | "renega"
      | "desconstrói"
      | "despreza"
      | "desaloca"
;


s-apesar-de: "apesar de "$artigo>indefine-artigo
           | "não obstante "$artigo>possessiviza-artigo
;


adverbio-posjustifica: ""
                     | ", " ?sub=s-sentido s-apesar-de " " $sub " mais " adjetivo-informal("m")
;

s-sentido: "sentido" ?artigo="o"
;

tambem-evidente-em: "é também evidente em"
                  | "surge novamente em"
                  | "aparece também em"
                  | "pode ser notad"$artigo " também em"
;

in-termo: "que prevalece em"
        | "intrínsec"$artigo " a"
        | "retratad"$artigo " em"
        | "que é tema central em"
;

existe: "existe"
      | "pode ser " encontrado
;

existe-plural: "existem"
             | "podem ser " encontrado"s"
;

encontrado: "encontrad"$artigo
          | "descobert"$artigo
          | "revelad"$artigo
;

promove: "promove"
       | "sugere"
       | "estimula"
;


denotar: "denotar "
       | "explicitar "
       | "implicar "
       | "sugerir "
;

temos: "temos"[", "entao", "|" "]"de "
     | "devemos" [", "entao", "|" "]
     | "precisamos"[", "entao", "|" "]
;

escolher: "escolher"
        | "optar"
        | "selecionar"
;


// per se
per-se: " tal e qual"
      | " por si"
      | " como tal"
      | ", como " intelectual " diria"
      | ?sub=termo ", como " $artigo " " $sub " sugere"
      | ""
;

// in-fact
de-fato: ", de fato,"
       | ""
;


// modifier-prefix
prefixo-modificador: "pós-"
                   | "neo-"
                   | "sub"
                   | "pré-"
                   | "socio-"
                   | "proto-"
                   | "meta-"
;


// something between
algo-entre: "diferença" ?artigo="a"
          | "ponte" ?artigo="a"
          | "terreno comum" ?artigo="o"
;


// thus
entao: "então"
     | "logo"
     | "portanto"
;

dualismo: "liberdade"
        | "aprisionamento"
        | "o abstrato"
        | "o concreto"
        | "internalidade"
        | "externalidade"
        | "criação"
        | "destruição"
        | "masculinidade"
        | "feminilidade"
;


// opposite
oposto: "liberdade" <-> "aprisionamento"
        "o abstrato" <-> "o concreto"
        "internalidade" <-> "externalidade" 
        "criação" <-> "destruição"
        "masculinidade" <-> "feminilidade"
;


// something-of
algo-de: ?sub=algo-de2
         $artigo " " $sub

       | ?sub=algo-de2
         $artigo " " $sub ", e subsequentemente "
         ?sub=algo-de2 
         $artigo " " $sub //","

       | ?sub=algo-de2
         $artigo " " $sub ", e " entao " "
         ?sub=algo-de2 
         $artigo " " $sub //","

       | ?sub=algo-de2
         $artigo " " $sub ", e " 
         ["eventualmente" | "com o tempo" | "alguns diriam que"] " "
         ?sub=algo-de2 
         $artigo " " $sub //","
;


// something-of-2
algo-de2: "fracasso" ?artigo="o"
        | "futilidade" ?artigo="a"
        | "colapso" ?artigo="o"
        | "fracasso" ?artigo="o"
        | "extâse" ?artigo="o"
        | "insensatez" ?artigo="a"
        | "absurdidade" ?artigo="a"
        | "paradigma" ?artigo="o"
        | "gênero" ?artigo="o"
        | "característica definidora" ?artigo="a"
        | "dialética" ?artigo="a"
        | "economia" ?artigo="a"
;


//preamble
preambulo: "porém, "
         | "pode-se dizer que "
         | "de certo modo, "
         | "já "
         //FIXME
         | "os " adjetivo-base2"istas deram um passo mais, visto que "
;

ligacao: ", porém "
       | ", mas "
       | ", mesmo se "
       | ", entretanto "
       | ", no entanto "
       | ", todavia "
       | ", mas "
       | ", portanto "
       | ", logo "

;

// however
entretanto: " "
          | ", entretanto, "
          | ", no entanto, "
          | ", contudo, "
          | ", todavia, "
          | ", porém, "
;


entretanto-forcado: ", entretanto, "
                  | ", no entanto, "
                  | ", contudo, "
                  | ", todavia, "
                  | ", porém, "
;




// result
resultado: resultado2
         | resultado2 poscondicao
;

// result-2
resultado2: ?sub=objeto-abstrato-importante
            $artigo " " $sub " " usado-para fim

          | ?sub=objeto-nebuloso
            $artigo " " $sub " " 
            ?art=$artigo
            ?sub=fonte
            vem-de($art) " " $sub

          | ?sub=objeto-importante 
            $artigo " " $sub adverbio-opcional " tem " 
            ?sub=propriedade
            artigo-indefinido-opcional " " $sub

          | ?sub=objeto-abstrato-ou-instituicao
            $artigo " " $sub 
            ?sub=estado-de-ser
            " " $conj " " $sub

          |?sub=proposito
            $artigo " " $sub " "
            ?sub=papel
            $artigo>preposicao-de " " $sub
            ?sub=objetivo
            " " $conj " " $artigo " " $sub

          |?sub=objeto-abstrato-ou-instituicao
            $artigo " " $sub
            ?sub=capacidade
            " é " s-capaz " de " ["gerar" | "produzir"]  " " 
            $artigo>indefine-artigo " " $sub
;

// result--1
resultado1: resultado
            | "nós podemos assumir que " resultado
            | "o modelo de " intelectual 
              ?sub=termo
              " para " $artigo " " $sub 
              ?sub=novo-termo
              " é "$artigo>indefine-artigo
              " \"" $sub "\", e " entao " " estado-de-ser
;


// assumption
suposicao: termo
         | "trabalho de " intelectual " sobre " 
           ?sub=termo 
           $artigo " " $sub ?artigo="o"
         | "premissa d" ?sub=termo $artigo " " $sub ?artigo="a"
;

// relation
relacao: "é igual "$artigo>preposicao-a
       | "é distint"$artigo " d"$artigo
       | "é intercambiável com " $artigo
;


       

// prim-condition
precondicao: ?sub=suposicao $artigo " " $sub " " 
             $artigo>verbo-ser " " adjetivo-validade

           | ?sub=objeto-abstrato-importante 
             $artigo " " $sub " " relacao " "
             ?sub=objeto-abstrato-importante 
             " " $sub
;

// corollary
corolario: "; se aquilo não é o caso, " resultado1
         | "; de outro modo, " resultado1
         | ""
; 


// postcondition
poscondicao: ", dado que " precondicao
           | ", mas somente se " precondicao corolario
           | ", já que " precondicao
           | ""
;


// state-of-being
estado-de-ser: estado-de-ser2
             | adverbio-abstrato " " estado-de-ser2 ?conj<<"é"
             | ?sub=algo-de2 "parte d"$artigo " " $sub ?sub=objeto-abstrato-importante " d"$artigo " " objeto-abstrato-importante ?conj=""
;




// state-of-being-2
estado-de-ser2: ?sub=bogeyman "serve "$artigo>preposicao-a " " $sub ?conj=""
              | ?sub=bogeyman "responsável pel"$artigo " " $sub ?conj="é"
              | "impossível" ?conj="é"
              | "inexpressiv"$artigo ?conj="é"
              | "inatingível" ?conj="é"
              | "elitista" ?conj="é"
              | "uma ficção legal" ?conj="é"
              | "mort"$artigo ?conj="está"
;

// property
propriedade: "significado intrínseco" ?artigo="o"
           | "significância" ?artigo="a"
           | "valor objetivo" ?artigo="o"
;

// ends
fim: ?sub=vitima verbo-negativo>verbo-para-infinitivo " " $artigo " " $sub
   | ?sub=bogeyman pos-verbo-negativo>verbo-para-infinitivo " " $artigo " " $sub
;


// implies-that
implica-que: "implica que "
           | "afirma que "
           | "mantém que "
           | "sugere que "
;

// is-used-to
usado-para: " é usad"$artigo " para "
          | " serve para "
          | " pode ser usad"$artigo " para "
;


// comes-from
vem-de(art): " vem d"$artigo " "
      | " tem de vir d"$artigo " "
      | " é produto d"$artigo " "
      | " é criad"art " pel"$artigo " "
;

// source
fonte: "comunicação" ?artigo="a"
     | "inconsciente coletivo" ?artigo="o"
     | "massas" ?artigo="as"
;

// purpose-word
proposito: "propósito" ?artigo="o"
         | "objetivo" ?artigo="o"
         | "razão de ser" ?artigo="a"
         | "tarefa" ?artigo="a"
         | "significância" ?artigo="a"
;


// role
papel: "artista" ?artigo="o"
     | "observador" ?artigo="o"
     | "participante" ?artigo="o"
     | "leitor" ?artigo="o"
     | "poeta" ?artigo="o"
     | "escritor" ?artigo="o"
;


// goal
objetivo: "forma significante" ?artigo="a" ?conj="é"
        | "desconstrução" ?artigo="a" ?conj="é"
        | "comentário social" ?artigo="o" ?conj="é"
;


// capability
capacidade: objetivo
          | intento
          | "verdade" ?artigo="a"
          | "significância" ?artigo="a"
;

// intento
intento: "intento" ?artigo="o"
       | "intenção" ?artigo="a"
       | "intencionalidade" ?artigo="a"
;


// Retorna um novo termo para topico frasal, ou um dos pré-definidos
termo: novo-termo
     | $v-assunto ?artigo=$v-artigo
     | $v-assunto2 ?artigo=$v-artigo2
     | $v-assunto3 ?artigo=$v-artigo3
; 


novo-termo: ?sub=substantivo-abstrato
            ?gen=$artigo>genero-por-artigo
            $sub " " adjetivo($gen)

          | ?sub=substantivo-abstrato
            ?gen=$artigo>genero-por-artigo
            $sub " " adjetivo($gen)

          | ?artigo="a"
            "teoria " adjetivo("f") " " adjetivo("f")

          | ?sub=objeto-nebuloso
            ?gen="m"
            "paradigma " adjetivo("m") " " $artigo>preposicao-de " " $sub
            ?artigo="o"

          | ?sub=ideologia
            ?gen=$artigo>genero-por-artigo
            $sub " " adjetivo($gen)

          | termo-intelectual(intelectual)
;

termo1: ?sub=substantivo-abstrato
        ?gen=$artigo>genero-por-artigo
       
        $artigo " " $sub " " adjetivo($gen);

termo2: ?sub=substantivo-abstrato 
        ?gen=$artigo>genero-por-artigo
       
        [$artigo>indefine-artigo | $artigo] " " $sub " " adjetivo($gen);


// SUBSTITUIÇÕES ÚTEIS

remove-espacos-iniciais: "^ *.*" -> "^ "/"";

remove-nao-inicial: "^.*não" -> "não"/"";

remove-virgula: ".*,$" -> ",$"/""
                "^,.*" -> "^,"/""
;

remove-ponto: ".*\. $" -> "\. $"/""

;

preposicao-a: "a$" -> "a$"/"à"
              "o$" -> "o$"/"ao"
              "as$" -> "as$"/"às"
              "os$" -> "os$"/"aos"
;

preposicao-de: "a$" -> "a$"/"da"
               "o$" -> "o$"/"do"
               "as$" -> "as$"/"das"
               "os$" -> "os$"/"dos"
;

preposicao-em: "a$" -> "a$"/"na"
               "o$" -> "o$"/"no"
               "as$" -> "as$"/"nas"
               "os$" -> "os$"/"nos"
;


verbo-ser: "a$" -> "é"
           "o$" -> "é"
           "as$" -> "são"
           "os$" -> "são"
;



indefine-artigo: "a$" -> "a$"/"uma"
                 "o$" -> "o$"/"um"
                 "as$" -> "as$"/"umas"
                 "os$" -> "os$"/"uns"
               
;

possessiviza-artigo: "a$" -> "a$"/"sua"
                     "o$" -> "o$"/"seu"
                     "as$" -> "as$"/"suas"
                     "os$" -> "os$"/"seus"
;

artigo-indefinido-opcional: $artigo>indefine-artigo
                          | ""
;


remove_vogal: ".*o$" -> "o$"/""
;

sufixo_ismo: ".*[aeiou]$" -> "[aeiou]$"/"ismo"
             ".*$"        -> "$"/"ismo"
;


prefixo_de: "^[aeiou].*" -> "^"/"des"
            "^.*"        -> "^"/"de"
;

adjetivizar_ismo: ".*ismo$" -> "ismo$"/"ista" 
;


criar_conceitos: ".*" -> "$"/"-conceito"
;

intelectual_ista: "Sartre$" -> "$"/"ano"
                  "Foucault$" -> "t$"/"diana"
                  "Derrida$" -> "$"/"ista"
                  ".*[aeiou]$" -> "[aeiou]$"/"ista"
                  ".*$" -> "$"/"ista"
;


termo-intelectual(i):  @i>criar_conceitos " " i>intelectual_ista$plural
;



verbo-para-infinitivo: // exceções vem primeiro
                       "oprime" -> "oprimir"
                      // regras genericas
                      ".*a$" -> "a$"/"ar"
                      ".*e$" -> "e$"/"er"
                      ".*i$" -> "i$"/"ir"
;

verbo-para-passado: // exceções vem primeiro
                    "oprime" -> "oprimido"
                   // regras genericas
                   ".*a$" -> "a$"/"ado"
                   ".*e$" -> "e$"/"ido"
                   ".*i$" -> "i$"/"ido"
;



// verbos para conceitos negativos

verbo-negativo: "marginaliza"
              | "explora"
              | "oprime"
              | "enfraquece"
;

verbo-positivo: "fortalece"
;


verbo-neutro: "interpola"
            | "contextualiza"
;


// verbos positivos para conceitos negativos
pos-verbo-negativo: "reforça"
                  | "entrincheira"
;





// vitimas
vitima: "minorias" ?artigo="as"
      | "desprivilegiados" ?artigo="os"
      | "proletariado" ?artigo="o"
;

bogeyman: "capitalismo" ?artigo="o"
        | "hierarquia"  ?artigo="a"
        | "'status quo'" ?artigo="o"
        | "divisões de classe" ?artigo="as"
        | "sexismo" ?artigo="o"
        | ?sub=objeto-importante
          ?gen=$sub>genero
          ?adjetivo_local=adjetivo-negativo($gen)
          ?artigo_local=artigo-definido($gen)
          ?adjetivo_local " percepção d"$artigo " " $sub 
;





// ADVERBIOS

adverbio-opcional: ""
                 | ", " adverbio ", "
;

adverbio: adverbio2 
        | "talvez " adverbio2 
        | "de certo modo " adverbio2
;

adverbio2: "paradoxalmente"
         | "surpreendentemente"
         | "ironicamente"
         
;

adverbio-negativo: "levianamente"
                 | "escandalosamente"
;


adverbio-abstrato: "fundamentalmente"
                 | "intrinsecamente"
;


//ADJETIVOS

pluralizar-adjetivo: ".*al$" -> "al$"/"ais"
                     ".*a$" -> "a$"/"as"
                     ".*o$" -> "o$"/"os"
                     ".*$" -> "$"/"!FIXME!"
;


adjetivo-concreto(gen): @gen>adjetivo-concreto-escolha
                      | adjetivo-concreto-n
;


adjetivo-concreto-escolha: "f" -> "adjetivo-concreto-f"
                           "m" -> "adjetivo-concreto-m"
;

adjetivo-concreto-f: adjetivo-concreto-base>remove_vogal "a" 
;

adjetivo-concreto-m: adjetivo-concreto-base>remove_vogal "o" 
;


adjetivo-concreto-n: "circular"
                   | "flamejante"
;

adjetivo-concreto-base: "quebrado"
                      | "esquecido"
                      | "pétreo"
                      | "férreo"
                      | "abandonado"
                      | "ignorado"
                      | "enganado"
;



adjetivo-numerico-plural: "um número de"
                        | "qualquer número de"
                        | "muit"$artigo"s"
                        | "uma abundância de"
                        | "vári"$artigo"s"
                        | "cada vez mais"
;


adjetivo-validade: adjetivo-validade-base>remove_vogal $artigo
;

adjetivo-validade-base: "válido"
                      | "inválido"
;


adjetivo-negativo(gen): @gen>adjetivo-negativo-escolha
                      | adjetivo-negativo-n
;

adjetivo-negativo-n: "sexista"
                   | "colonialista"
                   | "elitista"
                   | "'demodê'"
                   | "incognoscível"
                   | "críptico"
                   | "implausível"
                   | "segregacionista"
                   | "pueril"
                   | "obscurantista"

;


adjetivo-negativo-escolha: "f" -> "adjetivo-negativo-f"
                           "m" -> "adjetivo-negativo-m"
;

adjetivo-negativo-f:  adjetivo-negativo-base>remove_vogal "a"
;


adjetivo-negativo-m:  adjetivo-negativo-base>remove_vogal "o"
;


adjetivo-negativo-base: "ultrapassado"
                      | "arcaico"
                      | "problemático"
                      | "defasado"
                      | "ingênuo"
                      | "equivocado"
                      | "obscuro"
                      | "hermético"
                      | "assimétrico"
;
 


adjetivo-informal(gen): 
@gen>adjetivo-escolha
                      | adjetivo-n
                      | "auto-"auto-adjetivo
                      | "mitopoético"
;


auto-adjetivo: "referencial"
             | "suficiente"
             | "justificável"
             | "sustentável" 
             | "falseável"
//  fullfilling?
;


adjetivo(gen): @gen>adjetivo-escolha
             | adjetivo-n
             | prefixo-modificador adjetivo-n
             | prefixo-modificador @gen>adjetivo-escolha
;

adjetivo-escolha: "f" -> "adjetivo-f"
                  "m"  -> "adjetivo-m"
;

adjetivo-n: adjetivo-base2
          | "capitalista"
;

adjetivo-m: adjetivo-base>remove_vogal "o"
;

adjetivo-f: adjetivo-base>remove_vogal "a"
;


// adjetivos que podem ter gênero mudado trocando o "o" final por "a"
adjetivo-base: "heterogêneo"
             | "analítico"
             | "assertórico"
             | "distinto"
             | "semiótico"
             | "dialético"
             | "moderno"
             | "construtivo"
             | "semântico"
             | "desconstrutivo"
;

// adjetivos que não têm genero e podem ser transformados em adjetivo 
// e substantivo acrescentando "ista" e "ismo"
adjetivo-base2: "estrutural"
              | "patriarcal"
              | "conceitual"
              | "material"
              | "cultural"
              | "textual"

;

// ARTIGOS

artigo-definido(gen): gen>artigo-definido-escolha;

artigo-indefinido(gen): gen>artigo-indefinido-escolha;


artigo-definido-escolha: "f" -> "a"
                         "m" -> "o"
;

artigo-indefinido-escolha: "f" -> "uma"
                           "m" -> "um"
;


// SUBSTANTIVOS
pluralizar: ".*ão$" -> "ão$"/"ões"
            ".*a$" -> "a$"/"as"
            ".*o$" -> "o$"/"os"
            ".*a$" -> "a$"/"as"
            ".*e$" -> "e$"/"es"
;


substantivo-concreto: "porta" ?artigo="a"
                    | "fruta" ?artigo="a"
                    | "chave" ?artigo="a"
                    | "céu" ?artigo="o"
                    | "mar" ?artigo="o"
                    | "casa" ?artigo="a"
                    | "muro" ?artigo="o"
                    | "ramo" ?artigo="o"
;


substantivo-abstrato: substantivo-abstrato2
                    | "teoria" ?artigo="a"
                    | "discurso" ?artigo="o"
                    | "narrativa" ?artigo="a"
                    | substantivo-abstrato2>prefixo_de
;

substantivo-abstrato2: "sublimação" ?artigo="a"
                     | "materialismo" ?artigo="o"
                     | "situacionismo" ?artigo="o"
                     | "construção" ?artigo="a"
                     | "apropriação" ?artigo="a"
                     | adjetivo-base2>sufixo_ismo ?artigo="o"
;


ideologia: "capitalismo" ?artigo="o"
         | "Marxismo" ?artigo="o"
         | "socialismo" ?artigo="o"
         | "feminismo" ?artigo="o"
         | "libertarianismo" ?artigo="o"
         | "objetivismo" ?artigo="o"
         | "racionalismo" ?artigo="o"
         | "nacionalismo" ?artigo="o"
         | "niilismo" ?artigo="o"
;

movimento-artistico: "surrealismo" ?artigo="o"
                   | "modernismo" ?artigo="o"
                   | "realismo" ?artigo="o"
                   | "social-realismo" ?artigo="o"
                   | "construtivismo" ?artigo="o"
                   | "expressionismo" ?artigo="o"
;

objeto-nebuloso: "realidade" ?artigo="a"
               | "discurso" ?artigo="o"
               | "consenso" ?artigo="o"
               | "expressão" ?artigo="a"
               | "narrativa" ?artigo="a"
               | "contexto" ?artigo="o"
;

objeto-singular: "realidade" ?artigo="a"
               | "totalidade" ?artigo="a"
               | "paradoxo" ?artigo="o"
               | "completude" ?artigo="a"
               | "complexidade" ?artigo="a"
               | "globalização" ?artigo="a"
               | "progresso" ?artigo="o"
;
 
objeto-importante: "sociedade" ?artigo="a"
                 | "classe" ?artigo="a"
                 | objeto-abstrato-importante
                 | "identidade sexual" ?artigo="a"
;

objeto-abstrato-ou-instituicao: objeto-abstrato-importante
                              | instituicao
;


objeto-abstrato-importante: "cultura" ?artigo="a"
                          | "linguagem" ?artigo="a"
                          | "arte" ?artigo="a"
                          | "realidade" ?artigo="a"
                          | "verdade" ?artigo="a"
                          | "sexualidade" ?artigo="a"
                          | "narratividade" ?artigo="a"
                          | "consciência" ?artigo="a"
                          | "estética" ?artigo="a"
                          | "metafísica" ?artigo="a"
                          | "ética" ?artigo="a"
;

instituicao: "Constituicao" ?artigo="a"
           | "mídia" ?artigo="a"
           | "meio acadêmico" ?artigo="o"
           | "lei" ?artigo="a"
           | "governo" ?artigo="o"
           | "Estado" ?artigo="o"
           | "coletivo" ?artigo="o"
           | "estabelecido" ?artigo="o"
           | "bem-comum" ?artigo="o"
;



// SELECIONA GENERO DO SUBSTANTIVO
// exceções devem vir antes

genero-por-artigo: "a" -> "f"
                   "as" -> "f"
                   "uma" -> "f"
                   "umas" -> "f"
                   "o" -> "m"
                   "os" -> "m"
                   "um" -> "m"
                   "uns" -> "m"
;

genero: //exceções
	".*ismo$" -> "m"
        //regras
        ".*ão$"   -> "f"
        ".*o$"    -> "m"
        ".*a$"    -> "f"
        ".*e$"    -> "f"
        ".*"      -> "m" 
;



// notas de rodapé
opt-ed: "" | "ed. "
;

rodape-cita-texto(sobrenome): sobrenome ", " iniciais opt-ed "(" rodape-ano ")" ITALIC([rodape-titulo "."]) " " rodape-editora;

rodape-cita(sobrenome): FOOTNOTE(rodape-cita-texto(sobrenome));


rodape-editora: "Casa Jorge Editorial" |
                "Forense Universitária" |
                "Gryphus Editora" |
                "Jorge Zahar Editor" |
                "Editora Musa" |
                "Editora Nórdica" |
                "Editora Objetiva" |
                "Editora Pallas" |
                "Editora Campus" |
                "Editora Pensamento" | 
                "Editora Record" |
                "Editora Relume-Dumará" |
                "Editora Renovar" |
                "Editora Revan" |
                "Editora Rocco" |
                "Editora Temas & Idéias" |
                "UFRJ" |
                "Editora Tal" ;



rodape-ano: "19" decada digito;

decada: "7"|"8";

digito: "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9";


fonte-de-ideia: intelectual
              | intelectual-classico
              | autor
;


intelectual-classico: "Platão"
                    | "Voltaire"
                    | "Nietzsche"
                    | "Kant"
                    | "Hegel"
                    | "Hume" 
;


intelectual: "Lacan"
           | "Derrida"
           | "Baudrillard"
           | "Sartre"
           | "Foucault"
           | "Marx"
           | "Debord"
           | "Bataille"
           | "Lyotard"
           | "Sontag"
;



autor: "Lodge"
     | "Huyssen"
     | "Cooke"
     | "Owens"
     | "Johnston"
     | "Olsen"
     | "Giddens"
     | "Milner"
;  


artista: artista-citavel 
       | artista-nao-citavel
;

artista-citavel: "Burroughs"
               | "Joyce"
               | "Gibson"
               | "Stone" 
               | "Pynchon" 
               | "Spelling" 
               | "Tarantino" 
               | "Madonna"
               | "Rushdie" 
               | "Eco" 
;

artista-nao-citavel: "Koons" 
                   | "Mapplethorpe" 
                   | "Glass" 
                   | "Lynch" 
                   | "Fellini"
                   | "Cage" 
                   | "McLaren" 
;



// works of citable artists

Spelling-works:  "Beverly Hills 90210" | "Melrose Place" | "Models, Inc." ;

Pynchon-works: "Gravity's Rainbow" | "Vineland" | "The Crying of Lot 49" ;

Stone-works: "JFK" | "Natural Born Killers" | "Heaven and Earth" | "Platoon" ;

Tarantino-works: "Reservoir Dogs" | "Pulp Fiction" | "Clerks" ;

Fellini-works:
        "8 1/2" // I remembered this because the Plan 9 window system is named
                // after it
;

Burroughs-works:        "The Naked Lunch"  | "The Soft Machine" | "Queer"
        | "Port of Saints" | "Junky" | "The Ticket that Exploded"
        | "Nova Express" | "The Last Words of Dutch Schultz"
;

Joyce-works:    "Ulysses" | "Finnegan's Wake"
;

Gibson-works:   "Neuromancer" | "The Burning Chrome" | "Mona Lisa Overdrive"
        | "Virtual Light";

Madonna-works:  "Erotica" | "Sex" | "Material Girl" ;

Rushdie-works: "Satanic Verses" | "Midnight's Children" ;

Eco-works: "The Name of the Rose" | "Foucault's Pendulum" ;


// trabalhos

Spelling-trabalhos:  "Barrados no Baile"
                  | "Melrose" 

;

Pynchon-trabalhos: "Gravity's Rainbow" 
             | "Vineland" 
             | "The Crying of Lot 49" 
;

Stone-trabalhos: "JFK" 
               | "Assassinos por Natureza" 
               | "Entre o Céu e a Terra" 
               | "Platoon" 
;

Tarantino-trabalhos: "Cães de Aluguel" 
                   | "Pulp Fiction" 
                   | "Jackie Brown" 
;

Fellini-trabalhos: "A Doce Vida"
                 | "Mulheres e Luzes"
                 | "Oito e Meio"
;

Burroughs-trabalhos: "The Naked Lunch"  
                   | "The Soft Machine" 
                   | "Queer"
                   | "Port of Saints" 
                   | "Junky" 
                   | "The Ticket that Exploded"
                   | "Nova Express" 
                   | "The Last Words of Dutch Schultz"
;

Joyce-trabalhos: "Ulysses" 
               | "Finnegan's Wake"
;

Gibson-trabalhos: "Neuromancer" 
                | "The Burning Chrome"
                | "Mona Lisa Overdrive"
                | "Virtual Light"
;

Madonna-trabalhos: "Erotica" 
                 | "Sex" 
                 | "Material Girl" 
;

Rushdie-trabalhos: "Versos Satânicos"
                 | "Os Filhos da Meia-Noite"
;

Eco-trabalhos: "O Nome da Rosa"
             | "O Pêndulo de Foucault"
             | "Baudolino"
;


// conceitos
Lacan-conceito: "obscuridade" ?artigo="a" ?plural=""
;

Derrida-conceito: "leitura" ?artigo="a"  ?plural=""
;

Baudrillard-conceito: "simulação" ?artigo="a" ?plural=""
                    | "simulacro" ?artigo="a" ?plural=""
                    | "hiper-realidade" ?artigo="a" ?plural=""
;

Sartre-conceito: "absurdo" ?artigo="o" ?plural=""
               | "existencialismo" ?artigo="o" ?plural=""
;

Foucault-conceito: "relações de poder" ?artigo="as" ?plural="s"
;

Marx-conceito: "capitalismo" ?artigo="o" ?plural=""
             | "socialismo" ?artigo="o" ?plural=""
             | "classe" ?artigo="a" ?plural=""
;

Debord-conceito: "imagem" ?artigo="a" ?plural=""
               | "situação" ?artigo="a" ?plural=""
;

Bataille-conceito: "'comunicação'" ?artigo="a" ?plural=""
;

Lyotard-conceito: "narrativa" ?artigo="a" ?plural=""
;

Sontag-conceito: "campo" ?artigo="o" ?plural=""
;



// NOMES


nome: primeiro-nome " " sobrenome-generico
    | primeiro-nome " " inicial* sobrenome-generico
    | primeiro-nome " " sobrenome-generico
;


primeiro-nome:
"Alexandre"|"Adriano"|"Adolfo"|"Augusto"|"Armando"|
"Charles"|"Carlos"|"Cássio"|"Celena"|"Constantino"|
"Eloisa"|"David"|"Dionisio"|"Demétrio"|"Edson"|"Eduardo"|
"Estevão"|"Emilio"|"Fausto"|"Fábio"|"Felício"|
"Gabriel"|"Gilberto"|"Guilherme"|"Haroldo"|"Hercules"|"Horacio"|
"Ivani"|"Inacio"|"Irineu"|"José"|"João"|"Jaime"|"Laércio"|
"Leandro"|"Lucas"|
"Mariano"|"Marcelo"|"Murilo"|"Mauricio"|"Narciso"|"Nelson"|
"Odair"|"Osmar"|"Otávio"|
"Pedro"|"Percival"|"Plínio"|"Rafael"|"Reinaldo"|"Ricardo"|
"Ronaldo"|"Rômulo"|
"Sidney"|"Silvio"|"Tarcisio"|"Tales"|"Valentino"|"Vladimir"
;


sobrenome-generico: 
"Abreu"|"Aguiar"|"Alencar"|"Andrade"|"Amorim"|"Araújo"|"Azevedo"|
"Baltazar"|"Barbosa"|"Bittar"|"Bittencourt"|"Borges"|
"Campos"|"Cachoeira"|"Cândido"|"Carvalho"|
"Deluca"|"Duarte"|"Dutra"|
"Espindola"|
"Fagundes"|"Ferreira"|"Fortunato"|"Fritz"|"Freitas"|
"Garcia"|"Gasparetto"|"Gesser"|"Gomes"|"Gonçalves"|
"Halla"|"Hammes"|"Hoffmann"|
"Inácio"|
"Justino"|"Justo"|
"Klein"|"Koch"|
"Laranja"|"Lima"|"Leal"|"Levi"|"Lourdes"|
"Macedo"|"Machado"|"Monteiro"|"Marques"|"Medeiros"|"Molinari"|"Moraes"|
"Nascimento"|"Neves"|"Nunes"|
"Oliveira"|"Onofre"|
"Pacheco"|"Paiva"|"Pires"|"Pinto"|
"Rabelo"|"Rezende"|"Ribeiro"|"Rocha"|
"Sabino"|"Salvador"|"Santos"|"Silva"|"Soares"|
"Teixeira"|"Tramontina"|
"Vargas"|"Vieira"|"Vicente"|"Vitorete"|
"Wagner"|
"Xavier"|
"Zanon"|"Zunino"
;


inicial: "A. " | "B. " | "C. " | "D. " | "E. " | "F. " | "G. " | "H. "
        | "I. " | "J. " | "K. " | "L. " | "M. " | "N. " | "O. " | "P. "
        | "Q. " | "R. " | "S. " | "T. " | "U. " | "V. " | "W. "
        | "Y. " | "Z. "
;


iniciais: inicial+;


