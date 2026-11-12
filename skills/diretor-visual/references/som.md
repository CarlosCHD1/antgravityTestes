# Som

O espectador perdoa uma imagem imperfeita e abandona um som ruim. Em filme narrado, o som carrega a emoção e a imagem carrega o sentido, e os dois precisam ser dirigidos com o mesmo cuidado.

## As quatro camadas

| Camada | Função | Observação |
|---|---|---|
| Voz | Conduz a história | Sempre a camada mais clara e mais próxima |
| Música | Define o estado emocional e o andamento | Vale tanto pela entrada quanto pela saída |
| Ambiente | Dá lugar e continuidade às imagens | O som do espaço, que une planos diferentes na mesma cena |
| Efeitos e ruídos | Dão corpo aos gestos e objetos | Passos, tecido, ferramenta, papel, o que os americanos chamam de foley |

## Direção de voz

Descreva a voz no `05-som.md` com idade aparente, timbre, distância e andamento. Para o gênero, a referência é a voz próxima do microfone, de volume baixo e sem projeção, que soa como confidência. Marque no roteiro as palavras de peso, as pausas com duração em segundos e os trechos em que o ritmo muda.

Quando a voz for sintetizada, divida o texto em blocos curtos, gere cada bloco separadamente e ajuste as pausas na montagem. Blocos longos tendem a sair com entonação monótona. Evite números escritos em algarismos e siglas, que os sintetizadores costumam ler mal.

## Música

A música mais eficaz no documentário é a que o espectador quase não nota. Prefira instrumentação pequena, como piano, cordas sustentadas, violão ou texturas de sintetizador, a arranjos orquestrais crescentes, que soam como anúncio.

Planeje um mapa de música com três informações por trecho: o que toca, com que intensidade e por quê. Algumas decisões costumam funcionar. No vertical curto, deixe o primeiro segundo quase seco, só voz e um som, e traga a música depois que a frase de gancho terminou. Retire a música no instante da virada, porque o silêncio repentino faz o espectador se inclinar para a frente. Devolva a música no fechamento, mais simples do que estava antes.

No longo, evite música contínua. Alterne trechos com música, trechos só com ambiente e trechos de silêncio, e use a troca de tema musical para marcar a passagem de capítulo.

Corte a imagem em relação ao compasso com liberdade. Cortes sempre em cima da batida ficam mecânicos, e um corte ligeiramente antes do tempo forte dá mais impulso.

## Ambiente e ruídos

Imagens geradas nascem mudas, e é a ausência de som do mundo que as denuncia como artificiais. Para cada cena, defina um ambiente contínuo, como o interior de uma oficina com o tique-taque de vários relógios, e dois ou três ruídos sincronizados com gestos visíveis. Um plano detalhe de mão girando uma chave de fenda precisa do som desse metal.

Sons de impacto graves e sons crescentes de transição devem aparecer no máximo uma ou duas vezes no filme. Usados em toda troca de plano, perdem o efeito e deixam o vídeo com cara de modelo pronto.

## Silêncio

O silêncio é uma escolha de som. Há dois tipos úteis: o silêncio de música, em que ficam só voz e ambiente, e o silêncio de voz, em que ficam só imagem e ambiente. O segundo é o respiro. Coloque pelo menos um por minuto de filme, logo depois da frase mais importante de cada trecho.

## Mixagem

A voz fica na frente em todo momento. Como referência prática, a música sob narração deve ficar de 12 a 18 decibéis abaixo da voz e subir apenas nos trechos sem fala. O volume final para redes sociais fica em torno de menos 14 LUFS, com picos abaixo de menos 1 decibel. Ouça a mixagem no alto-falante do celular antes de publicar, porque é ali que a maioria vai escutar, e graves muito profundos simplesmente desaparecem.

## Quando o áudio já vem pronto

Com a narração ou o depoimento já gravado, a ordem do trabalho se inverte e a imagem passa a obedecer ao tempo do áudio. Siga estes passos.

Primeiro, obtenha a transcrição com marcação de tempo por frase, usando a ferramenta de transcrição ou de análise de áudio disponível na sessão. Se não houver nenhuma, peça ao usuário o texto e a duração total, e distribua o tempo proporcionalmente com `scripts/tempo_narracao.py`, avisando que os tempos são estimados.

Depois, ouça a estrutura pelo texto. Marque onde a voz respira, onde acelera, quais palavras recebem ênfase e onde há pausas maiores que meio segundo. Essas pausas são os pontos naturais de corte e os lugares onde um plano sem fala pode entrar.

Em seguida, agrupe as frases em batidas de sentido. Um plano não precisa trocar a cada frase. Ele troca quando muda a ideia, a emoção ou o tempo da história. Uma frase longa e importante pode atravessar dois planos, e três frases curtas de enumeração podem pedir três planos detalhe rápidos.

Então preencha o JSON com `modo_audio` igual a `audio_fornecido`, usando como duração de cada plano o intervalo real do áudio. O validador passa a comparar a soma dos planos com a duração do arquivo.

Por fim, avalie o áudio como diretor. Se a gravação tem ruído, trechos repetidos ou uma introdução longa antes de a história começar, diga isso e proponha os cortes. Em vídeo vertical, a história precisa começar no primeiro segundo, mesmo que para isso seja preciso remover a saudação gravada.

Quando o áudio é um depoimento, uma pregação ou um trecho de podcast, e não uma narração escrita para vídeo, escolha o trecho com começo, meio e virada, e trate o resto como material para outros vídeos.
