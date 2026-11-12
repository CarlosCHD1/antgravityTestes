# Identidade do canal

Este arquivo guarda as decisões que valem para todos os vídeos. Leia antes de montar a bíblia visual de qualquer episódio e use como padrão. Ele é feito para ser editado conforme o canal amadurece.

## Nome e promessa

O nome de trabalho é Histórias para Viver. A alternativa em avaliação é Histórias para Aprender. A decisão ainda está aberta, então não grave o nome em vinhetas ou cartelas definitivas até ela ser tomada.

A promessa do canal é contar histórias reais ou inspiradas em fatos, pequenas no tamanho e grandes no sentido, de onde o espectador sai com algo para a própria vida sem que ninguém precise dizer a lição em voz alta.

## Voz

O narrador é próximo e calmo, fala como quem conta algo a um amigo e não como quem apresenta um programa. Não usa frases de efeito, não faz perguntas retóricas em série e não fecha com moral explicada. O texto prefere o fato concreto ao adjetivo.

## Look da casa

O padrão é o naturalismo de prestígio descrito em `references/biblia-visual.md`. Cada episódio pode variar época, ambiente e paleta, mas mantém os elementos abaixo, que são a assinatura do canal.

| Elemento | Decisão da casa |
|---|---|
| Luz | Motivada e suave, com preferência por janela, fim de tarde e fontes práticas |
| Lentes | 35 mm para o mundo, 85 mm para pessoas, macro para detalhes |
| Câmera | Fixa ou em aproximação lenta, sem movimentos exibicionistas |
| Cor | Saturação contida, tons de pele fiéis, pretos levemente elevados |
| Textura | Grão fino de película em todos os planos |
| Abertura | Sempre em plano detalhe ou primeiro plano, nunca em paisagem |
| Fechamento | Uma imagem que rima com a abertura, seguida de um segundo de silêncio |
| Texto na tela | Mínimo, em fonte sem serifa de peso médio, sem animações chamativas |

## DNA visual padrão

Use este bloco como base do `dna_visual` e ajuste apenas o campo de cor ao episódio.

```json
{
  "estilo": "cinematic documentary still, photorealistic, naturalistic and restrained, prestige television look",
  "camera_e_lente": "shot on 35mm film with vintage prime lenses, shallow depth of field, natural perspective",
  "luz": "soft motivated light from windows and practical lamps, gentle falloff into shadow, never flat",
  "cor": "muted warm palette, true skin tones, lifted blacks, restrained saturation",
  "textura": "fine film grain, subtle halation on highlights, no digital sharpening",
  "negativo": "oversaturated, HDR, glossy commercial look, cartoon, illustration, 3D render, text, watermark, logo, lens flare, distorted hands"
}
```

## Formatos do canal

O formato principal é o vertical curto, de 45 a 90 segundos, publicado em Reels, Shorts e TikTok. O formato de aprofundamento é o horizontal, de 8 a 15 minutos, no YouTube. Quando uma história render os dois, o curto funciona como porta de entrada para o longo e não como resumo dele.

## O que o canal não faz

O canal não usa imagens genéricas de motivação, como montanhas ao amanhecer e multidões em câmera lenta. Não usa música épica crescente como muleta emocional. Não inventa fatos sobre pessoas reais e sinaliza quando uma história é inspirada em fatos ou é reconstituição. Não termina explicando o que a história quis dizer.
