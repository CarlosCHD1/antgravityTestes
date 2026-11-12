# Produção com IA

Este arquivo trata de como transformar a decupagem em imagens e vídeos gerados sem perder a consistência, e de quando preferir outras fontes.

## De onde vem cada imagem

Cada plano do JSON tem um campo `fonte`. Decida caso a caso.

| Fonte | Quando preferir |
|---|---|
| `gerado` | Reconstituições, atmosferas, detalhes, lugares e épocas sem registro disponível |
| `arquivo` | Fotos, documentos e vídeos reais da história, que sempre valem mais que qualquer recriação |
| `filmado` | Material captado pelo próprio usuário, mesmo com celular, quando a história é próxima dele |
| `stock` | Planos de cobertura genéricos, como cidade, natureza, mãos trabalhando |
| `grafismo` | Cartelas, mapas, linhas do tempo, texto animado |

Um material real imperfeito costuma ter mais força que um gerado impecável. Quando existir arquivo, construa o filme em torno dele e use a geração para o que falta.

## Anatomia do prompt de imagem

O exportador monta o prompt final nesta ordem, e é útil saber disso ao escrever `prompt_imagem`.

| Parte | De onde vem | Exemplo |
|---|---|---|
| Sujeito, ação e ambiente específicos | `prompt_imagem` do plano | weathered hands holding a pocket watch open under a brass desk lamp |
| Personagem | Descrição fixa em `personagens` | an 80-year-old Brazilian watchmaker with thin white hair and round wire glasses |
| Locação | Descrição fixa em `locacoes` | a cramped old watch repair shop with dark wood shelves full of clocks |
| Enquadramento, ângulo e lente | Campos do plano, traduzidos | detail insert shot, eye level, macro lens |
| DNA visual | Bloco `dna_visual` | estilo, câmera, luz, cor e textura do filme |
| Proporção | Dados do projeto | aspect ratio 9:16 |

Em `prompt_imagem`, escreva o que a câmera vê, em linguagem concreta e física. Descreva a ação congelada em um instante, a posição do sujeito no quadro, a fonte de luz específica daquela cena e um ou dois elementos de ambiente. Não escreva emoções abstratas, que o gerador não sabe fotografar. Em vez de pedir um homem triste, descreva os ombros caídos, o olhar para baixo e a xícara intocada.

Não repita no plano o que já está no DNA. Estilo dito duas vezes com palavras diferentes puxa a imagem para lados opostos.

## Consistência de personagem e de lugar

A consistência depende de quatro práticas somadas.

A primeira é a descrição literal idêntica, que o exportador já garante. A segunda é a imagem de referência: gere primeiro um retrato neutro do personagem e uma vista geral da locação, aprove, e use essas imagens como referência nas gerações seguintes, quando a ferramenta aceitar. A terceira é manter o mesmo modelo de geração e os mesmos parâmetros do início ao fim, porque trocar de modelo no meio muda a textura do filme. A quarta é decupar a favor da consistência, usando planos que reduzem a exposição do rosto quando a história permite, como mãos, costas, perfil em contraluz, silhueta e detalhes.

Essa última prática é também uma escolha de linguagem. Um personagem visto por fragmentos e de costas ganha mistério e universalidade, e o espectador se projeta nele com mais facilidade.

## Fluxo de geração

Trabalhe em quatro passagens, sempre consultando o custo antes de gerar, quando a ferramenta oferecer essa consulta.

Na primeira passagem, gere dois ou três quadros-chave: a abertura, um plano do personagem e o fechamento. Olhe cada resultado antes de seguir, compare com a bíblia e mostre ao usuário. Ajuste o DNA até esses quadros estarem certos, porque todo o resto herda deles.

Na segunda, gere as imagens paradas de todos os planos, usando os quadros aprovados como referência de estilo. Revise o conjunto lado a lado e refaça os que destoam em cor, luz ou fisionomia.

Na terceira, anime as imagens aprovadas, convertendo imagem em vídeo. Use `prompt_movimento` com uma instrução curta e única, como slow push-in on the hands, dust drifting in the light. Mantenha os clipes entre três e seis segundos e descreva apenas o que se move. Planos que funcionam bem parados podem receber só o movimento lento de câmera na edição, o que é mais barato e mais estável.

Na quarta, gere a voz, a música e os efeitos, seguindo `som.md`, e monte.

Quando não houver ferramenta de geração na sessão, entregue `export/prompts.md` e explique essa mesma ordem para o usuário executar na ferramenta que ele usa.

## Problemas frequentes

| Problema | Correção |
|---|---|
| O rosto muda de um plano para outro | Reforçar a referência de imagem, reduzir planos frontais, decupar por fragmentos |
| Mãos e dedos deformados | Simplificar o gesto, fechar o enquadramento, esconder parte da mão atrás do objeto |
| Texto ilegível dentro da imagem | Não pedir texto ao gerador. Aplicar cartelas e letreiros na edição |
| Imagem com cara de publicidade | Conferir o campo negativo, pedir luz motivada, reduzir a saturação, acrescentar imperfeições como poeira e desgaste |
| Cada plano com uma cor diferente | Fixar a paleta no DNA com nomes de cor e igualar na correção de cor |
| Movimento deformando a cena | Pedir um movimento só, mais lento, e encurtar o clipe |
| Época errada em roupas e objetos | Escrever a década e o lugar na descrição da locação e do personagem |

## Compromisso com o real

Documentário é um pacto de confiança com quem assiste, e esse pacto é o maior patrimônio de um canal de histórias.

Imagem gerada que representa um acontecimento real é reconstituição. Trate assim, com uma estética que não se faça passar por registro autêntico, e sinalize na descrição do vídeo ou em cartela quando houver risco de confusão. As plataformas também exigem a marcação de conteúdo realista gerado por IA, e vale usar a opção própria de cada uma na hora de publicar.

Não gere o rosto de uma pessoa real identificável, nem crie falas, documentos ou fotos falsas atribuídas a alguém que existe. Para personagens reais, use arquivo quando houver e, quando não houver, recorra a silhuetas, detalhes, objetos e lugares.

Diferencie no texto o que é fato, o que é relato e o que é inspirado em fatos. Uma história ficcional contada como parábola deve ser apresentada assim. Quando a história envolver dor de pessoas reais, pergunte ao usuário de onde ela vem e se há consentimento para contá-la.

Confira direitos de uso de músicas, imagens de arquivo e material de banco antes de publicar.
