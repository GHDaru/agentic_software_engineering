#!/usr/bin/env python3
"""confere.py — portão de papéis e skills (capítulo 7).

Confere um "time" de agentes descrito em arquivos (modelo operacional + perfis + skills)
contra dez regras e, depois, prova por mutação que cada regra acusa quando violada.

Regras de papel:
  P1  norma -> executável: todo papel de agente do modelo tem um perfil que o entrega
  P2  executável -> norma: todo perfil entrega um papel que o modelo prescreve
  P3  juiz sem caneta: perfil que julga não tem Write/Edit (Bash: só aviso)
  P4  contrato completo: Faz / Não faz / Consome / Produz / Entrega a
  P5  estreito: o perfil cabe no teto de linhas
  P6  modelo declarado: o papel diz em que faixa de modelo roda (pequeno|medio|grande)
Regras de skill:
  S1  gatilho: a description diz "Use quando"
  S2  lei de ferro: bloco de código sob "Lei de ferro", "Violar a letra" e >= 2 desculpas fechadas
  S3  nascimento: dor declarada em "nasceu-de" e linha de base com SEM e COM a skill
  S4  consumo: toda skill tem quem a consuma, e todo perfil cita só skills que existem

Só biblioteca padrão. Uso: python confere.py [pasta-do-time]   (padrão: ./time)
Saída: 0 = time conforme E todas as mutações acusadas; 1 = não.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

TETO_LINHAS = 40
FAIXAS = {"pequeno", "medio", "grande"}
SECOES = ["Faz:", "Não faz:", "Consome:", "Produz:", "Entrega a:"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def frente(texto):
    """Lê o front matter '---' simples (chave: valor) e devolve (campos, corpo)."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        return {}, texto
    campos = {}
    for linha in m.group(1).splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1)
            campos[k.strip()] = v.strip()
    return campos, m.group(2)


def lista(valor):
    return [x.strip() for x in valor.split(",") if x.strip()]


def papeis_do_modelo(time):
    """Papéis de AGENTE: linhas da tabela cuja coluna 'Exercido por' começa com 'Agente'."""
    texto = (time / "modelo-operacional.md").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"^\| \*\*(.+?)\*\* \| ([^|]+)\|", texto, re.M):
        if m.group(2).strip().startswith("Agente"):
            out.append(m.group(1))
    return out


def carrega(time):
    perfis = {}
    for f in sorted((time / "papeis").glob("*.md")):
        texto = f.read_text(encoding="utf-8")
        campos, corpo = frente(texto)
        perfis[f.stem] = {"campos": campos, "corpo": corpo, "linhas": len(texto.splitlines()),
                          "chars": len(texto.encode("utf-8"))}
    skills = {}
    for f in sorted((time / "skills").glob("*/SKILL.md")):
        texto = f.read_text(encoding="utf-8")
        campos, corpo = frente(texto)
        skills[f.parent.name] = {"campos": campos, "corpo": corpo, "pasta": f.parent}
    return perfis, skills


def confere(time):
    """Devolve (falhas, avisos): listas de (regra, mensagem)."""
    falhas, avisos = [], []
    prescritos = papeis_do_modelo(time)
    perfis, skills = carrega(time)
    entregues = {p["campos"].get("papel", ""): nome for nome, p in perfis.items()}

    for papel in prescritos:
        if papel not in entregues:
            falhas.append(("P1", f"'{papel}' é prescrito pelo modelo e nenhum perfil o entrega"))
    for papel, nome in sorted(entregues.items()):
        if papel not in prescritos:
            falhas.append(("P2", f"perfil '{nome}' entrega '{papel}', que o modelo não prescreve"))

    for nome, p in perfis.items():
        c = p["campos"]
        ferramentas = lista(c.get("ferramentas", ""))
        if c.get("julga") == "sim":
            caneta = [t for t in ferramentas if t in ("Write", "Edit")]
            if caneta:
                falhas.append(("P3", f"'{nome}' julga e tem {'/'.join(caneta)}"))
            if "Bash" in ferramentas:
                avisos.append(("P3", f"'{nome}' julga e tem Bash: o shell também escreve"))
        faltam = [s for s in SECOES if not re.search(rf"(^|\s){re.escape(s)}", p["corpo"], re.M)]
        if faltam:
            falhas.append(("P4", f"'{nome}' sem: {', '.join(faltam)}"))
        if p["linhas"] > TETO_LINHAS:
            falhas.append(("P5", f"'{nome}' tem {p['linhas']} linhas (teto {TETO_LINHAS})"))
        if c.get("modelo") not in FAIXAS:
            falhas.append(("P6", f"'{nome}' não declara a faixa de modelo (pequeno|medio|grande)"))

    consumidas = set()
    for nome, p in perfis.items():
        for s in lista(p["campos"].get("skills", "")):
            consumidas.add(s)
            if s not in skills:
                falhas.append(("S4", f"'{nome}' cita a skill '{s}', que não existe"))

    for nome, s in skills.items():
        c, corpo = s["campos"], s["corpo"]
        if "Use quando" not in c.get("description", ""):
            falhas.append(("S1", f"skill '{nome}' sem gatilho ('Use quando') na description"))
        lei = re.search(r"^## Lei de ferro\s*\n+```\n(.+?)\n```", corpo, re.S | re.M)
        desculpas = re.findall(r'^- "', corpo, re.M)
        if not lei or "Violar a letra" not in corpo or len(desculpas) < 2:
            falhas.append(("S2", f"skill '{nome}' sem lei de ferro completa "
                                 f"(lei={'sim' if lei else 'não'}, desculpas fechadas={len(desculpas)})"))
        base = s["pasta"] / c.get("linha-de-base", "-")
        if not c.get("nasceu-de"):
            falhas.append(("S3", f"skill '{nome}' não diz de que dor nasceu"))
        if not base.is_file():
            falhas.append(("S3", f"skill '{nome}' sem linha de base ({c.get('linha-de-base', 'ausente')})"))
        else:
            b = base.read_text(encoding="utf-8")
            if "SEM a skill" not in b or "COM a skill" not in b:
                falhas.append(("S3", f"skill '{nome}': a linha de base não registra SEM e COM a skill"))
        if nome not in consumidas:
            falhas.append(("S4", f"skill '{nome}' não é consumida por nenhum papel (skill órfã)"))
    return falhas, avisos, perfis


# --- mutações: cada uma quebra uma regra numa cópia do time e espera que ELA acuse ---------

def _troca(arq, de, para):
    t = arq.read_text(encoding="utf-8")
    assert de in t, f"mutação inválida: '{de}' não está em {arq.name}"
    arq.write_text(t.replace(de, para, 1), encoding="utf-8")


MUTACOES = [
    ("M1 o papel de interface perde o agente", "P1",
     lambda t: (t / "papeis" / "semantica-de-interface.md").unlink()),
    ("M2 o modelo deixa de citar a segurança", "P2",
     lambda t: _troca(t / "modelo-operacional.md", "| **Segurança** | Agente |", "| Segurança (fora) | Agente |")),
    ("M3 o revisor ganha caneta", "P3",
     lambda t: _troca(t / "papeis" / "revisor.md", "ferramentas: Read, Grep, Glob", "ferramentas: Read, Edit, Grep, Glob")),
    ("M4 o implementador perde o 'Não faz'", "P4",
     lambda t: _troca(t / "papeis" / "implementador.md", "Não faz:", "Observação:")),
    ("M5 o arquiteto incha", "P5",
     lambda t: _troca(t / "papeis" / "arquiteto.md", "Não faz:", "- regra extra\n" * 25 + "Não faz:")),
    ("M6 o especificador esquece o modelo", "P6",
     lambda t: _troca(t / "papeis" / "especificador.md", "modelo: medio\n", "")),
    ("M7 a skill perde o gatilho", "S1",
     lambda t: _troca(t / "skills" / "criterio-verificavel" / "SKILL.md", "Use quando", "Serve para")),
    ("M8 a lei vira sugestão", "S2",
     lambda t: _troca(t / "skills" / "diagnosticar-antes-de-consertar" / "SKILL.md",
                      "Violar a letra é violar o espírito.", "Considere investigar antes.")),
    ("M9 a skill nasce sem linha de base", "S3",
     lambda t: (t / "skills" / "criterio-verificavel" / "linha-de-base.md").unlink()),
    ("M10 ninguém consome a skill", "S4",
     lambda t: [_troca(t / "papeis" / n, l, r) for n, l, r in [
         ("implementador.md", "skills: diagnosticar-antes-de-consertar", "skills: criterio-verificavel"),
         ("revisor.md", "skills: criterio-verificavel, diagnosticar-antes-de-consertar", "skills: criterio-verificavel"),
         ("seguranca.md", "skills: diagnosticar-antes-de-consertar", "skills: criterio-verificavel")]]),
]


def main():
    time = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "time"
    falhas, avisos, perfis = confere(time)

    print("== papel × modelo × custo fixo de contexto")
    print(f"  {'perfil':<24}{'julga':<7}{'modelo':<9}{'linhas':>7}{'~tokens':>9}")
    for nome, p in perfis.items():
        c = p["campos"]
        print(f"  {nome:<24}{c.get('julga', '?'):<7}{c.get('modelo', '—'):<9}"
              f"{p['linhas']:>7}{round(p['chars'] / 4):>9}")
    tot_l = sum(p["linhas"] for p in perfis.values())
    tot_t = sum(round(p["chars"] / 4) for p in perfis.values())
    print(f"  {'total':<40}{tot_l:>7}{tot_t:>9}")

    print("\n== o time como está")
    for regra, msg in avisos:
        print(f"  aviso {regra} {msg}")
    for regra, msg in falhas:
        print(f"  ✗ {regra} {msg}")
    conforme = not falhas
    print("  ✓ dez regras conformes" if conforme else f"  ✗ {len(falhas)} falha(s)")

    print("\n== mutações (cada uma deve ser acusada pela SUA regra)")
    acusadas = 0
    for nome, regra, muta in MUTACOES:
        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp) / "time"
            shutil.copytree(time, copia)
            muta(copia)
            f, _, _ = confere(copia)
        regras = sorted({r for r, _ in f})
        ok = regra in regras
        acusadas += ok
        detalhe = next((m for r, m in f if r == regra), "nada acusou")
        print(f"  {'✓' if ok else '✗'} {nome}: {regra} {'acusou' if ok else 'NÃO acusou'} — {detalhe}")
    print(f"\nresultado: time {'conforme' if conforme else 'NÃO conforme'} · "
          f"mutações acusadas: {acusadas}/{len(MUTACOES)}")
    sys.exit(0 if conforme and acusadas == len(MUTACOES) else 1)


if __name__ == "__main__":
    main()
