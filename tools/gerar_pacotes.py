#!/usr/bin/env python3
"""Gera em dist/ os pacotes da skill para cada ferramenta.

Uso: python tools/gerar_pacotes.py
"""
import os
import re
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, "skills", "diretor-visual")
DIST = os.path.join(RAIZ, "dist")
ORDEM_REFS = ["narrativa", "linguagem-visual", "biblia-visual", "formatos", "som", "montagem", "producao-ia", "glossario"]


def ler(*partes):
    with open(os.path.join(*partes), encoding="utf-8") as f:
        return f.read()


def arquivos_da_skill():
    for pasta, _, nomes in os.walk(SKILL):
        if "__pycache__" in pasta:
            continue
        for n in sorted(nomes):
            caminho = os.path.join(pasta, n)
            yield caminho, os.path.relpath(caminho, SKILL)


def zip_pasta(destino, prefixo):
    """Skill inteira dentro de um zip, sob o prefixo indicado."""
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for caminho, rel in arquivos_da_skill():
            z.write(caminho, os.path.join(prefixo, rel))


def zip_chatgpt(destino):
    """Instruções para colar e arquivos de conhecimento sem subpastas."""
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(RAIZ, "adaptacoes", "chatgpt-instrucoes.md"), "1-instrucoes-para-colar.md")
        for caminho, rel in arquivos_da_skill():
            z.write(caminho, os.path.join("2-arquivos-de-conhecimento", os.path.basename(rel)))


def rebaixar(md):
    """Desce um nível os títulos, para caberem como seções de um documento único."""
    return re.sub(r"^(#+) ", r"#\1 ", md, flags=re.M)


def prompt_unico(destino):
    corpo = re.sub(r"^---.*?---\s*", "", ler(SKILL, "SKILL.md"), flags=re.S)
    partes = [
        "# Diretor visual, versão em arquivo único\n",
        "Este documento reúne o método completo em um só texto, para ferramentas que não carregam "
        "pastas de skill. Use como instrução de sistema ou envie no início da conversa. Onde o texto "
        "citar um arquivo de `references/` ou `assets/`, o conteúdo está nas partes seguintes deste "
        "mesmo documento.\n",
        "Se o ambiente não executar Python, faça as verificações dos scripts manualmente. Estime a "
        "narração a 150 palavras por minuto. Na decupagem, confira que o primeiro plano do vertical "
        "dura até 3 segundos, que nenhum plano passa de 6 segundos no vertical ou 15 no horizontal "
        "sem ser um respiro intencional, que a narração não passa de 3,2 palavras por segundo em "
        "nenhum plano, que não há três enquadramentos iguais seguidos, que existe ao menos um plano "
        "fechado e um plano sem narração, e que todo plano tem intenção escrita. Monte cada prompt "
        "final nesta ordem: descrição do plano, descrição fixa dos personagens, descrição fixa da "
        "locação, enquadramento com ângulo e lente em inglês, os cinco campos do DNA visual e a "
        "proporção. O DNA deve ser colado de forma idêntica em todos os prompts.\n",
        "# Parte 1. Método\n", rebaixar(corpo),
        "\n# Parte 2. Identidade do canal\n", rebaixar(ler(SKILL, "assets", "canal.md")),
    ]
    for i, ref in enumerate(ORDEM_REFS, 3):
        partes += [f"\n# Parte {i}. references/{ref}.md\n", rebaixar(ler(SKILL, "references", ref + ".md"))]
    partes += [
        f"\n# Parte {len(ORDEM_REFS) + 3}. assets/exemplo-decupagem.json\n",
        "```json\n" + ler(SKILL, "assets", "exemplo-decupagem.json").strip() + "\n```\n",
    ]
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))


def main():
    os.makedirs(DIST, exist_ok=True)
    zip_pasta(os.path.join(DIST, "diretor-visual.skill"), "diretor-visual")
    zip_pasta(os.path.join(DIST, "diretor-visual-antigravity.zip"), os.path.join(".agent", "skills", "diretor-visual"))
    zip_chatgpt(os.path.join(DIST, "diretor-visual-chatgpt.zip"))
    prompt_unico(os.path.join(DIST, "diretor-visual-arquivo-unico.md"))
    for n in sorted(os.listdir(DIST)):
        print(f"{os.path.getsize(os.path.join(DIST, n)):>8} bytes  dist/{n}")


if __name__ == "__main__":
    main()
