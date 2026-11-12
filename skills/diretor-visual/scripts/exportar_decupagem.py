#!/usr/bin/env python3
"""Exporta a decupagem em JSON para os arquivos de produção.

Uso:
    python exportar_decupagem.py 04-decupagem.json --saida export/

Gera:
    decupagem.md   tabela de planos com tempo, para leitura e filmagem
    decupagem.csv  a mesma tabela para planilha
    prompts.md     prompt final de imagem e de movimento de cada plano
    narracao.txt   texto corrido da narração, para gravação ou síntese de voz

O prompt final de cada plano é montado aqui, somando a descrição específica do
plano, as descrições fixas de personagens e locação, o enquadramento traduzido
e o DNA visual. Assim o estilo é idêntico em todos os planos por construção.
"""
import argparse
import csv
import json
import os

ENQ = {
    "GPG": ("Grande plano geral", "extreme wide shot"),
    "PG": ("Plano geral", "wide shot"),
    "PC": ("Plano conjunto", "full shot"),
    "PA": ("Plano americano", "cowboy shot framed from the knees up"),
    "PM": ("Plano médio", "medium shot"),
    "MPP": ("Meio primeiro plano", "medium close-up"),
    "PP": ("Primeiro plano", "close-up"),
    "PPP": ("Primeiríssimo plano", "extreme close-up"),
    "PD": ("Plano detalhe", "detail insert shot"),
}
ANG = {
    "nivel": "eye level",
    "plongee": "high angle looking down",
    "contra-plongee": "low angle looking up",
    "zenital": "top-down overhead view",
    "nadir": "worm's-eye view",
    "holandes": "dutch angle",
    "ombro": "over-the-shoulder",
    "pov": "point-of-view shot",
    "perfil": "profile view",
    "costas": "seen from behind",
    "frontal": "frontal, subject looking into the lens",
}


def tc(s):
    m, r = divmod(s, 60)
    return f"{int(m):02d}:{r:04.1f}"


def limpar(t):
    return str(t or "").strip().rstrip(".")


def prompt_final(pl, d):
    partes = [limpar(pl.get("prompt_imagem"))]
    for p in pl.get("personagens", []):
        partes.append(limpar(d.get("personagens", {}).get(p, {}).get("descricao")))
    if pl.get("locacao"):
        partes.append(limpar(d.get("locacoes", {}).get(pl["locacao"], {}).get("descricao")))
    camera = [ENQ.get(pl.get("enquadramento"), (None, limpar(pl.get("enquadramento"))))[1]]
    if pl.get("angulo"):
        camera.append(ANG.get(pl["angulo"], limpar(pl["angulo"])))
    if pl.get("lente"):
        lente = limpar(pl["lente"])
        camera.append(lente if "lens" in lente else f"{lente} lens")
    partes.append(", ".join(c for c in camera if c))
    dna = d.get("dna_visual", {})
    for campo in ("estilo", "camera_e_lente", "luz", "cor", "textura"):
        partes.append(limpar(dna.get(campo)))
    partes.append(f"aspect ratio {d['projeto'].get('proporcao', '9:16')}")
    return ". ".join(p for p in partes if p) + "."


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("arquivo")
    ap.add_argument("--saida", default="export")
    a = ap.parse_args()

    with open(a.arquivo, encoding="utf-8") as f:
        d = json.load(f)
    os.makedirs(a.saida, exist_ok=True)
    proj, planos = d["projeto"], d["planos"]
    colunas = ["id", "tempo", "dur.", "ato", "enquadramento", "ângulo", "lente", "movimento",
               "ação", "narração", "intenção", "som", "texto na tela", "transição", "fonte"]

    linhas, t = [], 0.0
    for pl in planos:
        dur = pl.get("duracao_s") or 0
        linhas.append([
            pl.get("id", ""), tc(t), f"{dur:g}s", pl.get("ato", ""),
            ENQ.get(pl.get("enquadramento"), (pl.get("enquadramento", ""),))[0],
            pl.get("angulo", ""), pl.get("lente", ""), pl.get("movimento", ""),
            pl.get("acao", ""), pl.get("narracao", ""), pl.get("intencao", ""),
            pl.get("som", ""), pl.get("texto_tela", ""), pl.get("transicao", ""),
            pl.get("fonte", "gerado"),
        ])
        t += dur

    with open(os.path.join(a.saida, "decupagem.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(colunas)
        w.writerows(linhas)

    esc = lambda v: str(v).replace("|", "/").replace("\n", " ")
    with open(os.path.join(a.saida, "decupagem.md"), "w", encoding="utf-8") as f:
        f.write(f"# Decupagem: {proj.get('titulo', '')}\n\n")
        f.write(f"Formato {proj.get('formato', '')} {proj.get('proporcao', '')}, {len(planos)} planos, "
                f"duração total de {tc(t)}.\n\n")
        f.write("| " + " | ".join(colunas) + " |\n")
        f.write("|" + "---|" * len(colunas) + "\n")
        for l in linhas:
            f.write("| " + " | ".join(esc(v) for v in l) + " |\n")

    negativo = limpar(d.get("dna_visual", {}).get("negativo"))
    with open(os.path.join(a.saida, "prompts.md"), "w", encoding="utf-8") as f:
        f.write(f"# Prompts: {proj.get('titulo', '')}\n\n")
        f.write("Gere primeiro os quadros-chave, aprove o look e use essas imagens como referência nos demais planos.\n\n")
        if negativo:
            f.write(f"Prompt negativo para todos os planos:\n\n```\n{negativo}\n```\n\n")
        for pl in planos:
            fonte = pl.get("fonte", "gerado")
            f.write(f"## Plano {pl.get('id', '')} ({pl.get('duracao_s', 0):g}s, {fonte})\n\n")
            f.write(f"{pl.get('acao', '')}\n\n")
            if fonte != "gerado":
                f.write(f"Este plano não é gerado. Fonte: {fonte}.\n\n")
                continue
            f.write(f"Imagem:\n\n```\n{prompt_final(pl, d)}\n```\n\n")
            if pl.get("prompt_movimento"):
                f.write(f"Movimento, a partir da imagem aprovada:\n\n```\n{limpar(pl['prompt_movimento'])}.\n```\n\n")

    with open(os.path.join(a.saida, "narracao.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(pl["narracao"].strip() for pl in planos if (pl.get("narracao") or "").strip()) + "\n")

    print(f"Exportado em {a.saida}/: decupagem.md, decupagem.csv, prompts.md, narracao.txt")
    print(f"{len(planos)} planos, duração total de {tc(t)}")


if __name__ == "__main__":
    main()
