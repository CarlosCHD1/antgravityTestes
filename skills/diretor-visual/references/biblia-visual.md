# Bíblia visual

A bíblia visual é o documento que fixa o look do filme antes de qualquer plano ser desenhado. É ela que faz vinte imagens produzidas em momentos diferentes parecerem filmadas pela mesma equipe, no mesmo dia, com a mesma câmera.

## Por que restringir

Consistência percebida é resultado de poucas variáveis repetidas. Um filme que usa cinco lentes, três lógicas de luz e uma paleta aberta parece uma coletânea. Um filme com duas lentes, uma lógica de luz e três cores parece ter autor. A bíblia existe para tomar essas decisões uma vez e proteger o filme das tentações de cada plano isolado.

Em um canal, a bíblia tem dois níveis. O primeiro é a identidade da casa, descrita em `assets/canal.md`, que vale para todos os vídeos e faz o público reconhecer o canal em dois segundos. O segundo é a variação do episódio, que ajusta paleta, época e ambiente à história contada sem quebrar a identidade.

## O que a bíblia contém

Escreva `03-biblia-visual.md` com as seções abaixo, em texto corrido e direto.

| Seção | O que definir |
|---|---|
| Conceito | Uma frase que resume o look e a razão dele para esta história |
| Referências | Dois ou três filmes, fotógrafos ou pintores, dizendo o que se toma de cada um |
| Câmera e lentes | Formato, as duas ou três distâncias focais permitidas, profundidade de campo, comportamento da câmera |
| Luz | A lógica geral, as fontes motivadas, o contraste, a hora do dia predominante |
| Cor | Dominante, secundária e acento, com códigos de cor, e o arco de cor se houver |
| Textura | Grão, nitidez, tratamento de altas luzes, tipo de película ou sensor que se imita |
| Personagens | Descrição física fixa de cada um, roupa, idade, traços, sempre com as mesmas palavras |
| Locações | Descrição fixa de cada ambiente, materiais, época, estado de conservação |
| Motivo visual | A imagem que retorna, e como ela muda a cada aparição |
| Tipografia e grafismo | Fonte, tamanho, posição e comportamento do texto na tela |
| Proibições | O que este filme nunca faz |

A seção de proibições é a mais subestimada. Escrever que o filme não usa câmera aérea, não usa câmera lenta fora da cena final e não mostra o rosto do personagem antes da virada dá mais identidade que qualquer lista de qualidades.

## Do documento ao DNA visual

O bloco `dna_visual` do JSON é a bíblia condensada em inglês, no formato que os geradores entendem. O exportador cola esse bloco no fim de todos os prompts, então ele deve conter apenas o que vale para o filme inteiro.

| Campo | Conteúdo | Exemplo |
|---|---|---|
| `estilo` | O meio e o gênero da imagem | cinematic documentary still, photorealistic, naturalistic and restrained |
| `camera_e_lente` | Câmera, película ou sensor, característica óptica | shot on 35mm film, vintage prime lenses, shallow depth of field |
| `luz` | A lógica de luz | soft motivated window light, gentle falloff into shadow, low-key |
| `cor` | Paleta e tratamento | muted warm palette of amber, walnut brown and faded teal, lifted blacks, true skin tones |
| `textura` | Acabamento | fine film grain, subtle halation, no digital sharpening |
| `negativo` | O que evitar | oversaturated, HDR, glossy, cartoon, illustration, text, watermark, lens flare |

Descreva personagens e locações com frases completas e reutilizáveis. A descrição de um personagem deve trazer idade aparente, tipo físico, cabelo, pele, um ou dois traços marcantes e a roupa. O exportador insere esse texto de forma idêntica em todos os planos onde o personagem aparece, e a repetição literal é o que mais ajuda o gerador a manter a mesma pessoa.

## Modelos de linguagem visual

Estes seis modelos são pontos de partida. Escolha o que serve à história e ajuste. Nenhum deles copia uma obra específica, todos descrevem famílias de decisões reconhecíveis.

| Modelo | Decisões principais | Serve para |
|---|---|---|
| Naturalismo de prestígio | Luz motivada e suave, 35 e 85 mm, paleta contida, câmera fixa ou em aproximação lenta, grão fino | Biografias, histórias de vida, a maior parte dos vídeos narrados |
| Claro-escuro investigativo | Baixa luz, sombras profundas, fontes práticas em quadro, tons frios com acento âmbar, quadros dentro de quadros | Mistérios, quedas, histórias de crime, viradas sombrias |
| Memória em película | Imitação de 16 mm ou Super 8, cores desbotadas e quentes, vinheta leve, câmera na mão suave, altas luzes leitosas | Infância, saudade, histórias de família, passado |
| Rigor contemplativo | Planos fixos e simétricos, grande profundidade de campo, planos gerais longos, quase nenhuma música | Ofícios, lugares, reflexão, histórias em que o tempo é o tema |
| Vérité urgente | Câmera na mão, 28 mm perto dos corpos, luz disponível, cortes secos, som direto em destaque | Superação, esporte, histórias em andamento, tensão física |
| Arquivo e reconstituição | Fotos e documentos com movimento lento, reconstituições em silhueta ou detalhe, cartelas sóbrias | História, personagens reais sem imagens disponíveis, fatos antigos |

## Como testar a bíblia

Antes de decupar, escreva três quadros-chave que representem o filme: o plano de abertura, um plano do personagem no meio da história e o plano final. Se os três couberem dentro das regras e ainda parecerem do mesmo filme, a bíblia está pronta. Se algum exigir uma exceção, a regra está errada ou o plano está, e é melhor descobrir isso agora.

Quando houver ferramenta de geração, produza esses três quadros primeiro e mostre ao usuário. O que for aprovado vira imagem de referência para todos os planos seguintes.
