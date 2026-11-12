#!/usr/bin/env python3
"""Valida uma decupagem em JSON e aponta problemas de estrutura, ritmo e direção.

Uso:
    python validar_decupagem.py 04-decupagem.json

Erros impedem a produção. Avisos são pontos para o diretor revisar e podem ser
mantidos quando forem escolha consciente. Sai com código 1 se houver erro.
"""
import json
import re
import statistics
import sys

ENQUADRAMENTOS = {"GPG", "PG", "PC", "PA", "PM", "MPP", "PP", "PPP", "PD"}
FECHADOS = {"PP", "PPP", "PD"}
FONTES = {"gerado", "arquivo", "filmado", "stock", "grafismo"}
DNA_CAMPOS = ["estilo", "camera_e_lente", "luz", "cor", "textura"]
# limites por formato: gancho máximo, plano máximo, faixa de duração média
LIMITES = {
    "vertical": {"gancho": 3.0, "plano": 6.0, "media": (1.5, 3.8)},
    "horizontal": {"gancho": 8.0, "plano": 15.0, "media": (3.5, 9.0)},
}
PALAVRAS_POR_SEGUNDO_MAX = 3.2


def validar(d):
    erros, avisos = [], []
    proj = d.get("projeto", {})
    planos = d.get("planos", [])
    formato = proj.get("formato")

    for campo in ("titulo", "formato", "proporcao", "duracao_alvo_s"):
        if not proj.get(campo):
            erros.append(f"projeto: falta o campo '{campo}'")
    if formato not in LIMITES:
        erros.append("projeto.formato deve ser 'vertical' ou 'horizontal'")
        formato = "vertical"
    lim = LIMITES[formato]

    dna = d.get("dna_visual", {})
    for campo in DNA_CAMPOS:
        if not dna.get(campo):
            erros.append(f"dna_visual: falta o campo '{campo}', sem ele os prompts perdem consistência")

    if not planos:
        erros.append("nenhum plano na decupagem")
        return erros, avisos

    personagens = d.get("personagens", {})
    locacoes = d.get("locacoes", {})
    ids = set()
    for i, pl in enumerate(planos):
        pid = str(pl.get("id", f"posição {i + 1}"))
        r = f"plano {pid}"
        if pid in ids:
            erros.append(f"{r}: id repetido")
        ids.add(pid)

        dur = pl.get("duracao_s")
        if not isinstance(dur, (int, float)) or dur <= 0:
            erros.append(f"{r}: duracao_s ausente ou inválida")
            pl["duracao_s"] = 0
            dur = 0

        if len(str(pl.get("intencao", "")).strip()) < 20:
            erros.append(f"{r}: sem intenção clara. Diga o que o espectador deve sentir e por que esta escolha produz isso")
        if not str(pl.get("acao", "")).strip():
            erros.append(f"{r}: falta 'acao', a descrição do que se vê")

        enq = pl.get("enquadramento")
        if enq not in ENQUADRAMENTOS:
            avisos.append(f"{r}: enquadramento '{enq}' fora dos códigos {sorted(ENQUADRAMENTOS)}")

        fonte = pl.get("fonte", "gerado")
        if fonte not in FONTES:
            avisos.append(f"{r}: fonte '{fonte}' desconhecida")
        if fonte == "gerado" and not str(pl.get("prompt_imagem", "")).strip():
            erros.append(f"{r}: fonte é 'gerado' mas falta 'prompt_imagem'")

        for p in pl.get("personagens", []):
            if p not in personagens:
                erros.append(f"{r}: personagem '{p}' não está definido em 'personagens'")
        loc = pl.get("locacao")
        if loc and loc not in locacoes:
            erros.append(f"{r}: locação '{loc}' não está definida em 'locacoes'")

        n = len(re.findall(r"\w+", pl.get("narracao", "") or ""))
        if dur and n / dur > PALAVRAS_POR_SEGUNDO_MAX:
            avisos.append(f"{r}: {n} palavras em {dur} s. A narração não cabe, alongue o plano ou corte texto")

        if dur > lim["plano"] and not pl.get("respiro"):
            avisos.append(f"{r}: {dur} s é longo para o formato {formato}. Se for intencional, marque \"respiro\": true")

    # ritmo geral
    duracoes = [pl["duracao_s"] for pl in planos]
    total = sum(duracoes)
    alvo = proj.get("duracao_alvo_s") or 0
    if alvo:
        if proj.get("modo_audio") == "audio_fornecido":
            if abs(total - alvo) > 0.5:
                erros.append(f"soma dos planos ({total:.1f} s) difere do áudio ({alvo} s). A imagem precisa fechar com o áudio")
        elif abs(total - alvo) / alvo > 0.08:
            avisos.append(f"soma dos planos ({total:.1f} s) está a mais de 8% da duração alvo ({alvo} s)")

    if duracoes[0] > lim["gancho"]:
        avisos.append(f"o primeiro plano dura {duracoes[0]} s. O gancho do formato {formato} pede até {lim['gancho']} s")
    if formato == "vertical" and not (planos[0].get("narracao") or planos[0].get("texto_tela")):
        avisos.append("o primeiro plano não tem narração nem texto na tela. No vertical o gancho precisa de palavra junto com a imagem")

    media = statistics.mean(duracoes)
    if len(planos) >= 5 and not lim["media"][0] <= media <= lim["media"][1]:
        avisos.append(f"duração média de plano de {media:.1f} s, fora da faixa {lim['media'][0]} a {lim['media'][1]} s do formato {formato}")

    # variedade
    enqs = [pl.get("enquadramento") for pl in planos]
    for i in range(len(enqs) - 2):
        if enqs[i] and enqs[i] == enqs[i + 1] == enqs[i + 2]:
            ids3 = ", ".join(str(planos[j].get("id")) for j in (i, i + 1, i + 2))
            avisos.append(f"planos {ids3}: três {enqs[i]} seguidos. Varie a escala ou justifique como sequência de montagem")
    if len(planos) > 6 and len(set(enqs)) < 3:
        avisos.append("menos de três enquadramentos diferentes no filme. Falta variação de escala")
    if len(planos) > 4 and not FECHADOS & set(enqs):
        avisos.append("nenhum plano fechado (PP, PPP ou PD). O filme fica sem intimidade")

    movs = [str(pl.get("movimento", "")).lower() for pl in planos]
    for i in range(len(movs) - 2):
        if movs[i] and "fix" not in movs[i] and movs[i] == movs[i + 1] == movs[i + 2]:
            avisos.append(f"o movimento '{movs[i]}' se repete em três planos seguidos a partir do {planos[i].get('id')}")
            break

    if len(planos) >= 6 and not any(not (pl.get("narracao") or "").strip() for pl in planos):
        avisos.append("todos os planos têm narração. Reserve ao menos um respiro só de imagem e som")

    return erros, avisos


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        d = json.load(f)
    erros, avisos = validar(d)
    planos = d.get("planos", [])
    total = sum(pl.get("duracao_s") or 0 for pl in planos)
    print(f"{d.get('projeto', {}).get('titulo', 'sem título')}: {len(planos)} planos, {total:.1f} s")
    for e in erros:
        print(f"  ERRO   {e}")
    for a in avisos:
        print(f"  AVISO  {a}")
    if not erros and not avisos:
        print("  Decupagem válida, sem apontamentos.")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
