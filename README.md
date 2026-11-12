# Diretor visual

Uma skill para o Claude que funciona como diretor e equipe de cinema documental para redes sociais. Você entrega a história, um roteiro ou um áudio gravado. Ela devolve o filme pensado por inteiro, do tratamento aos prompts de geração, com o mesmo estilo visual do primeiro ao último plano.

Foi construída para o canal de histórias, reflexão e motivação que tem como nome de trabalho Histórias para Viver, em vídeos verticais para Reels, Shorts e TikTok e em vídeos horizontais para o YouTube.

## O que ela entrega

Para cada história, um pacote de direção com seis documentos e uma pasta de exportação.

| Arquivo | Conteúdo |
|---|---|
| `01-tratamento.md` | Logline, pergunta dramática, tema, ponto de vista e ideia visual central |
| `02-roteiro.md` | Narração dividida em batidas, com tempo |
| `03-biblia-visual.md` | As regras do look, dos personagens e das locações |
| `04-decupagem.json` | Cada plano com enquadramento, ângulo, lente, movimento, ação e intenção |
| `05-som.md` | Direção de voz, música, desenho de som e silêncios |
| `06-montagem.md` | Ritmo, transições e texto na tela |
| `export/` | Tabela de planos, planilha, prompts finais e texto de narração |

## Como está organizada

A skill fica em `skills/diretor-visual/`. O arquivo `SKILL.md` conduz o trabalho na ordem de uma equipe real: direção, roteiro, fotografia e arte, decupagem, som, montagem, produção e continuidade. Cada departamento tem seu arquivo em `references/`, com o repertório técnico e a psicologia por trás de cada escolha.

Em `assets/` estão a identidade do canal, que serve de base para todos os vídeos, e um projeto de exemplo completo. Em `scripts/` estão três ferramentas em Python, sem dependências.

| Script | Função |
|---|---|
| `tempo_narracao.py` | Mede quanto tempo a narração ocupa e sugere a quantidade de planos |
| `validar_decupagem.py` | Aponta problemas de ritmo, repetição, narração que não cabe no plano e planos sem intenção |
| `exportar_decupagem.py` | Monta os prompts finais colando o DNA visual e as descrições fixas em todos os planos |

A consistência visual não depende de lembrar de repetir o estilo. O estilo é escrito uma vez e o exportador o insere em cada prompt.

## Como instalar

A pasta `dist/` traz um pacote para cada ferramenta. Todos são gerados a partir da mesma fonte com `python tools/gerar_pacotes.py`, então basta rodar esse comando depois de qualquer ajuste.

| Ferramenta | Arquivo | Como instalar |
|---|---|---|
| Claude | `diretor-visual.skill` | Em Configurações, na área de skills, envie o arquivo |
| Claude Code | nenhum | Abra este repositório, a skill já está ligada em `.claude/skills/` |
| Antigravity | `diretor-visual-antigravity.zip` | Extraia na raiz do projeto, o que cria `.agent/skills/diretor-visual/`. Para valer em todos os projetos, mova a pasta `diretor-visual` para `~/.gemini/antigravity/skills/` |
| ChatGPT | `diretor-visual-chatgpt.zip` | Crie um GPT ou um Projeto, cole o texto de `1-instrucoes-para-colar.md` nas instruções e envie os arquivos de `2-arquivos-de-conhecimento/`. No GPT, ative a execução de código |
| DeepSeek e outros chats | `diretor-visual-arquivo-unico.md` | Envie o arquivo no início da conversa, ou cole como instrução de sistema |
| Agentes de terminal | nenhum | Abra este repositório. O `AGENTS.md` da raiz aponta para a skill |

## Como usar

Conte a história e diga o formato. Por exemplo: "Quero um vídeo vertical de um minuto sobre o meu avô, que plantou uma árvore para cada neto." Ou envie um áudio já gravado e peça o vídeo em cima dele. Se não disser o formato, a skill assume vertical, de 45 a 75 segundos.

Para testar as ferramentas com o exemplo:

```bash
cd skills/diretor-visual
python scripts/validar_decupagem.py assets/exemplo-decupagem.json
python scripts/exportar_decupagem.py assets/exemplo-decupagem.json --saida export/
```

## Como ajustar

O arquivo `skills/diretor-visual/assets/canal.md` guarda o nome, a voz e o look da casa. Edite ali quando o nome do canal for decidido ou quando o estilo amadurecer, e gere o pacote de novo.
