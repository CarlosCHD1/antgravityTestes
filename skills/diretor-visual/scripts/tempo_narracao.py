#!/usr/bin/env python3
"""Estima a duração de uma narração e sugere a quantidade de planos.

Uso:
    python tempo_narracao.py roteiro.txt --ritmo documental --formato vertical
    python tempo_narracao.py roteiro.txt --duracao 58.4     (áudio já gravado)
    cat roteiro.txt | python tempo_narracao.py -

Cada parágrafo (bloco separado por linha em branco) é tratado como uma batida.
Com --duracao, o tempo real do áudio é distribuído entre as batidas na
proporção do número de palavras, o que serve de estimativa quando não há
transcrição com marcação de tempo.
"""
import argparse
import re
import sys

RITMOS = {"contemplativo": 130, "documental": 150, "curto": 170}
# duração média de plano (mínima, máxima) em segundos, por formato
PLANO_MEDIO = {"vertical": (1.5, 3.5), "horizontal": (4.0, 8.0)}


def fmt(segundos):
    m, s = divmod(segundos, 60)
    return f"{int(m):02d}:{s:04.1f}"


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("arquivo", help="arquivo de texto com a narração, ou - para ler da entrada padrão")
    p.add_argument("--ritmo", choices=RITMOS, default="documental")
    p.add_argument("--ppm", type=int, help="palavras por minuto (substitui --ritmo)")
    p.add_argument("--pausa", type=float, default=0.5, help="segundos de pausa entre batidas")
    p.add_argument("--formato", choices=PLANO_MEDIO, default="vertical")
    p.add_argument("--duracao", type=float, help="duração real do áudio em segundos")
    a = p.parse_args()

    texto = sys.stdin.read() if a.arquivo == "-" else open(a.arquivo, encoding="utf-8").read()
    # ignora títulos e marcações de markdown
    linhas = [l for l in texto.splitlines() if not l.lstrip().startswith(("#", "|", "```"))]
    batidas = [b.strip() for b in re.split(r"\n\s*\n", "\n".join(linhas)) if b.strip()]
    if not batidas:
        sys.exit("Nenhum texto encontrado.")

    palavras = [len(re.findall(r"\w+", b)) for b in batidas]
    total_palavras = sum(palavras)
    ppm = a.ppm or RITMOS[a.ritmo]

    if a.duracao:
        util = max(a.duracao - a.pausa * (len(batidas) - 1), 0.1)
        duracoes = [util * n / total_palavras for n in palavras]
        ppm = round(total_palavras / util * 60)
        origem = f"áudio de {a.duracao:.1f} s distribuído por proporção de palavras"
    else:
        duracoes = [n / ppm * 60 for n in palavras]
        origem = f"estimativa a {ppm} palavras por minuto"

    print(f"Narração: {total_palavras} palavras, {len(batidas)} batidas, {origem}\n")
    print(f"{'#':>2}  {'início':>7}  {'dur.':>5}  {'pal.':>4}  {'planos':>6}  texto")
    lo, hi = PLANO_MEDIO[a.formato]
    t = 0.0
    planos_min = planos_max = 0
    for i, (b, n, d) in enumerate(zip(batidas, palavras, duracoes), 1):
        pmin, pmax = max(1, round(d / hi)), max(1, round(d / lo))
        planos_min += pmin
        planos_max += pmax
        faixa = str(pmin) if pmin == pmax else f"{pmin}-{pmax}"
        resumo = " ".join(b.split())
        resumo = resumo if len(resumo) <= 60 else resumo[:57] + "..."
        print(f"{i:>2}  {fmt(t):>7}  {d:>4.1f}s  {n:>4}  {faixa:>6}  {resumo}")
        t += d + (a.pausa if i < len(batidas) else 0)

    print(f"\nDuração total com pausas: {fmt(t)} ({t:.1f} s)")
    print(f"Planos sugeridos para o formato {a.formato}: de {planos_min} a {planos_max}")
    if ppm > 185:
        print("Aviso: ritmo acima de 185 palavras por minuto. A narração vai soar corrida, corte texto.")
    if a.formato == "vertical" and t > 90:
        print("Aviso: acima de 90 s no vertical a retenção cai. Avalie cortar ou dividir em partes.")
    if a.formato == "vertical" and duracoes[0] > 4:
        print("Aviso: a primeira batida passa de 4 s. O gancho precisa caber nos primeiros 3 s.")


if __name__ == "__main__":
    main()
