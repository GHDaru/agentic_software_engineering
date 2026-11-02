"""partitura.py — a spec tratada como INSUMO, não como descrição (capítulo 4).

Só biblioteca padrão. Quatro subcomandos:

  lint <spec>              classifica cada requisito e critério: EARS, par (comando → esperado)
                           ou DESEJO (não verificável). Sai 1 se houver desejo.
  rastreio <spec> <teste>  requisito sem teste e teste sem requisito, nos dois sentidos.
                           Sai 1 se houver órfão.
  valor <spec> <FRn>       imprime o primeiro valor em R$ do requisito (o teste lê daqui).
  raia <mudancas.json>     decide a raia de cada mudança por ambiguidade × raio ×
                           irreversibilidade, com as regras de desempate.

A forma EARS aceita (em português): "QUANDO <condição>, O SISTEMA DEVE <comportamento>",
"ENQUANTO <estado>, O SISTEMA DEVE ...", "SE <condição indesejada>, ENTÃO O SISTEMA DEVE ...",
"ONDE <opcional>, O SISTEMA DEVE ..." e a ubíqua "O SISTEMA DEVE ...".
"""
import json
import re
import sys

EARS = re.compile(
    r"^(?:(QUANDO|ENQUANTO|ONDE) (?P<cond>.+?), |SE (?P<indesejada>.+?), ENTÃO )?"
    r"O SISTEMA DEVE (?P<comp>.+)$"
)
PAR = re.compile(r"^`[^`]+`\s*→\s*\S")
VAGAS = ("rápid", "intuitiv", "amigáve", "adequad", "eficiente", "satisfeit", "bom ", "boa ",
         "grande", "robust")
REQ = re.compile(r"^- \*\*(FR\d+)\*\*:\s*(.+)$")


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def requisitos(texto):
    """[(id, frase)] dos requisitos funcionais."""
    return [(m.group(1), m.group(2).strip()) for m in map(REQ.match, texto.splitlines()) if m]


def criterios(texto):
    """Itens de lista da seção de critérios de aceite."""
    out, dentro = [], False
    for linha in texto.splitlines():
        if linha.startswith("## "):
            dentro = linha.lower().startswith("## critérios de aceite")
            continue
        if dentro and linha.startswith("- "):
            out.append(linha[2:].strip())
    return out


def classificar(frase):
    frase = frase.rstrip(".")
    if PAR.match(frase):
        return "par", ""
    m = EARS.match(frase)
    if not m:
        return "desejo", "fora da forma EARS e sem comando que o prove"
    comp = m.group("comp").lower() + " "
    vaga = next((v.strip() for v in VAGAS if v in comp), None)
    if vaga:
        return "desejo", f"comportamento não observável ('{vaga}…')"
    return "ears", ""


def cmd_lint(spec):
    texto = ler(spec)
    itens = [(i, f) for i, f in requisitos(texto)] + [("critério", c) for c in criterios(texto)]
    desejos = 0
    print(f"lint {spec}")
    for ident, frase in itens:
        tipo, motivo = classificar(frase)
        if tipo == "desejo":
            desejos += 1
            print(f"  ✗ {ident:<8} DESEJO  {motivo}")
        else:
            print(f"  ✓ {ident:<8} {tipo.upper()}")
    if desejos:
        print(f"✗ {desejos} desejo(s): reescreva como QUANDO <condição>, O SISTEMA DEVE "
              f"<comportamento observável>, ou como `comando` → esperado.")
        return 1
    print(f"✓ {len(itens)} item(ns), todos verificáveis.")
    return 0


def cmd_rastreio(spec, teste):
    frs = [i for i, _ in requisitos(ler(spec))]
    testes = re.findall(r"^def test_(fr\d+)_\w*\(", ler(teste), re.M)
    cobertos = {t.upper() for t in testes}
    print(f"rastreio {spec} ↔ {teste}")
    falhas = 0
    for fr in frs:
        if fr in cobertos:
            print(f"  ✓ {fr} → test_{fr.lower()}_*")
        else:
            falhas += 1
            print(f"  ✗ {fr} sem teste: requisito que ninguém prova")
    for t in sorted(cobertos - set(frs)):
        falhas += 1
        print(f"  ✗ test_{t.lower()}_* sem requisito: código que a spec não pediu")
    if falhas:
        print(f"✗ {falhas} órfão(s) entre spec e teste.")
        return 1
    print(f"✓ {len(frs)} requisito(s), cada um com teste; nenhum teste sem requisito.")
    return 0


def valor(spec, fr):
    """Primeiro valor 'R$ 1.234,56' do requisito `fr`, como float."""
    for ident, frase in requisitos(ler(spec)):
        if ident == fr:
            m = re.search(r"R\$\s*([\d.]+,\d{2})", frase)
            if m:
                return float(m.group(1).replace(".", "").replace(",", "."))
            raise ValueError(f"{fr} não tem valor em R$")
    raise KeyError(f"{fr} não existe em {spec}")


NIVEL = {"baixa": 0, "baixo": 0, "media": 1, "médio": 1, "medio": 1, "média": 1,
         "alta": 2, "alto": 2}
SEMPRE_INFRA = {"infra", "migracao", "migração", "deploy"}


def decidir_raia(m):
    a, r, i = (NIVEL[m["ambiguidade"]], NIVEL[m["raio"]], NIVEL[m["irreversibilidade"]])
    fatores = f"amb={m['ambiguidade']} · raio={m['raio']} · irrev={m['irreversibilidade']}"
    tipo = m.get("tipo", "")
    if tipo in SEMPRE_INFRA:
        return "infra", fatores, f"{tipo} nunca é leve: plena + reversibilidade"
    if i == 2:
        return "infra", fatores, "irreversível: plena + reversibilidade"
    if a == r == i == 0:
        nota = "o pull request é o artefato"
        if tipo == "bug":
            nota += "; exige teste que reproduz o bug falhando antes"
        return "leve", fatores, nota
    if max(a, r, i) == 1 and a + r + i == 1:
        return "plena", fatores, "na dúvida entre leve e plena, plena"
    return "plena", fatores, "spec completa"


def cmd_raia(arquivo):
    with open(arquivo, encoding="utf-8") as f:
        mudancas = json.load(f)
    contagem = {}
    print(f"raia {arquivo}")
    for m in mudancas:
        raia, fatores, nota = decidir_raia(m)
        contagem[raia] = contagem.get(raia, 0) + 1
        print(f"  {raia:<6} {m['descricao']}")
        print(f"         {fatores} → {nota}")
    dist = " · ".join(f"{k}: {contagem.get(k, 0)}" for k in ("leve", "plena", "infra"))
    print(f"distribuição (visibilidade, nunca veredito): {dist}")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[0] == "lint":
        return cmd_lint(argv[1])
    if len(argv) >= 3 and argv[0] == "rastreio":
        return cmd_rastreio(argv[1], argv[2])
    if len(argv) >= 3 and argv[0] == "valor":
        print(f"{valor(argv[1], argv[2]):.2f}")
        return 0
    if len(argv) >= 2 and argv[0] == "raia":
        return cmd_raia(argv[1])
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    sys.exit(main(sys.argv[1:]))
