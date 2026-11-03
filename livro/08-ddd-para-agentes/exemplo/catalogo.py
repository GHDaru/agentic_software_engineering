#!/usr/bin/env python3
"""catalogo.py — o exemplo do capítulo 8: a linguagem ubíqua como artefato que a máquina lê.

Subcomandos (todos leem o modelo único, `modelo.json`; só biblioteca padrão):

  decidir  MODELO PROPOSTAS   cada nome que uma sessão de agente propõe recebe REUSE, ALIAS,
                              EXTEND ou CREATE — ou é recusado, com o motivo.
  lint     MODELO TEXTO       sigla nua ou sem dicionário, termo de família escrito nu,
                              apelido no lugar do termo do modelo.
  plano    PLAN.md            as quatro declarações de domínio (DOM:aggregate, invariants,
                              glossary, ports), cada uma com valor e motivo.
  endereco SESSOES CONSULTA…  resolve 'nome', 'nome · projeto' ou 'nome [ref] · projeto';
                              endereço ambíguo ou morto é RECUSADO, nunca adivinhado.
  glossario gerar MODELO      imprime o glossário gerado do modelo (com o sha256 do modelo).
  glossario conferir MODELO GLOSSARIO
                              regera do modelo e compara byte a byte; diz a linha que diverge.
  mutacao  MODELO             roda lint e plano sobre as fixtures boa e ruim de casos/ e diz
                              se as réguas discriminam.

Saída: 0 = conforme · 1 = achado (de propósito, em vários passos) · 2 = uso errado.
"""
import hashlib
import json
import re
import sys
from pathlib import Path


def carregar(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def chave(s):
    return " ".join(s.casefold().split())


# --------------------------------------------------------------------------- decidir
def decidir(modelo, propostas):
    termos = modelo["termos"]
    por_nome, por_apelido = {}, {}
    for t in termos:
        por_nome[chave(t["tela"])] = t
        por_nome[chave(t["codigo"])] = t
        for a in t["apelidos"]:
            por_apelido[chave(a)] = t
    familias = {chave(f): regra for f, regra in modelo["familias"].items()}
    contextos = modelo["contextos"]

    contagem = {"REUSE": 0, "ALIAS": 0, "EXTEND": 0, "CREATE": 0, "RECUSADO": 0}
    identificadores, novos, nomes = set(), [], []
    por_identificador = {}
    print(f"tarefa: {propostas['tarefa']}")
    for p in propostas["propostas"]:
        nome, k = p["nome"], chave(p["nome"])
        nomes.append(nome)
        primeira = k.split()[0]
        definido = bool(p.get("definicao")) and p.get("contexto") in contextos
        if k in por_nome:
            t = por_nome[k]
            dec, msg = "REUSE", f"já existe: {t['tela']} ({t['codigo']}, {t['contexto']})"
        elif k in por_apelido:
            t = por_apelido[k]
            dec, msg = "ALIAS", f"apelido de {t['tela']} ({t['codigo']}): use o termo do modelo"
        elif k in familias:
            t, dec, msg = None, "RECUSADO", f"termo nu — {familias[k]}"
        elif primeira in familias:
            t = None
            if definido:
                dec, msg = "EXTEND", f"nova forma qualificada da família '{primeira}' em {p['contexto']}: entra no modelo antes do código"
            else:
                dec, msg = "RECUSADO", f"extensão da família '{primeira}' sem definição ou sem contexto"
        else:
            t = None
            if definido:
                dec, msg = "CREATE", f"termo novo em {p['contexto']}, com definição: entra no modelo antes do código"
            else:
                dec, msg = "RECUSADO", "termo novo sem definição nem contexto — nome que ninguém definiu é o sinônimo de amanhã"
        contagem[dec] += 1
        if t is not None:
            identificadores.add(t["codigo"])
            por_identificador.setdefault(t["codigo"], set()).add(nome)
        elif dec in ("EXTEND", "CREATE"):
            identificadores.add(nome)
            novos.append(nome)
        marca = "✗" if dec == "RECUSADO" else "✓"
        print(f"  {marca} sessão {p['sessao']}  {nome:<22} {dec:<9} {msg}")

    print("resumo: " + " · ".join(f"{d} {n}" for d, n in contagem.items()))
    print(f"  {len(set(nomes))} nomes propostos por {len({p['sessao'] for p in propostas['propostas']})} sessões"
          f" → {len(identificadores)} identificadores ({len(novos)} novos, com definição)")
    for ident, ns in sorted(por_identificador.items()):
        if len(ns) > 1:
            print(f"  {len(ns)} nomes para {ident}: {', '.join(sorted(ns))}")
    return 1 if contagem["RECUSADO"] else 0


# --------------------------------------------------------------------------- lint
SIGLA = re.compile(r"\b[A-Z]{2,5}\b")


def achados_lint(modelo, texto):
    achados = []
    siglas = modelo["siglas"]
    vistas = set()
    termos_tela = [chave(t["tela"]) for t in modelo["termos"]]
    familias = modelo["familias"]
    apelidos = {a: t for t in modelo["termos"] for a in t["apelidos"]}
    for n, linha in enumerate(texto.splitlines(), 1):
        for m in SIGLA.finditer(linha):
            s = m.group(0)
            if s in vistas:
                continue
            vistas.add(s)
            if s not in siglas:
                achados.append((n, f"sigla sem dicionário: {s} (não está no modelo)"))
            elif chave(siglas[s]) not in chave(linha):
                achados.append((n, f"sigla nua na 1ª ocorrência: {s} — escreva '{siglas[s]} ({s})'"))
        baixa = chave(linha)
        for f, regra in familias.items():
            for m in re.finditer(rf"\b{re.escape(chave(f))}\b", baixa):
                resto = baixa[m.start():]
                if not any(resto.startswith(t) for t in termos_tela):
                    achados.append((n, f"termo nu: '{f}' — {regra}"))
        for a, t in apelidos.items():
            if re.search(rf"(?<!\w){re.escape(chave(a))}(?!\w)", baixa):
                achados.append((n, f"apelido '{a}' — o termo do modelo é '{t['tela']}' ({t['codigo']})"))
    return achados


def lint(modelo, caminho):
    achados = achados_lint(modelo, Path(caminho).read_text(encoding="utf-8"))
    print(f"lint {Path(caminho).name}")
    for n, msg in achados:
        print(f"  ✗ linha {n}: {msg}")
    if achados:
        print(f"✗ {len(achados)} achado(s).")
        return 1
    print("✓ nenhum achado: siglas expandidas, nenhum termo nu, nenhum apelido.")
    return 0


# --------------------------------------------------------------------------- plano
CHAVES = ["aggregate", "invariants", "glossary", "ports"]


def achados_plano(texto):
    achados, faltam = [], []
    linhas = texto.splitlines()
    for k in CHAVES:
        linha = next((l for l in linhas if f"DOM:{k}=" in l), None)  # a primeira, como o grep -m1
        if linha is None:
            faltam.append(k)
            continue
        valor = re.sub(rf".*DOM:{k}=([A-Za-z_-]*).*", r"\1", linha)
        motivo = re.sub(rf".*DOM:{k}=[A-Za-z_-]*", "", linha).replace("|", "").replace("`", "").strip()
        if not valor:
            achados.append(f"{k}: DOM:{k}= sem valor")
            continue
        if k == "invariants" and valor not in ("domain", "edge"):
            itens = re.sub(r".*DOM:invariants=", "", linha).replace("`", "").split("|")
            for it in (i.strip() for i in itens):
                if not it or re.fullmatch(r"[A-Za-z0-9_.-]+=domain", it) or re.fullmatch(r"[A-Za-z0-9_.-]+=edge\(.+\)", it):
                    continue
                if re.fullmatch(r"[A-Za-z0-9_.-]+=edge", it):
                    achados.append(f"invariants: '{it}' é borda sem motivo — escreva {it}(por que não pode ser domínio)")
                else:
                    achados.append(f"invariants: '{it}' — cada item é regra=domain ou regra=edge(porquê)")
            continue
        if not motivo or motivo.startswith("["):
            achados.append(f"{k}: DOM:{k}={valor} sem motivo — declaração sem porquê é silêncio")
    if faltam:
        achados.insert(0, "modelo de domínio nunca declarado: " + " ".join(faltam))
    return achados


def plano(caminho):
    achados = achados_plano(Path(caminho).read_text(encoding="utf-8"))
    print(f"plano {Path(caminho).name}")
    for a in achados:
        print(f"  ✗ {a}")
    if achados:
        print(f"✗ {len(achados)} achado(s).")
        return 1
    print("✓ modelo de domínio declarado (aggregate, invariants, glossary, ports), cada um com motivo.")
    return 0


# --------------------------------------------------------------------------- endereco
CONSULTA = re.compile(r"^\s*(?P<nome>[^\[·]+?)\s*(?:\[(?P<ref>\w+)\])?\s*(?:·\s*(?P<projeto>\S+))?\s*$")


def endereco(sessoes, consultas):
    falhou = 0
    for c in consultas:
        m = CONSULTA.match(c)
        if not m:
            print(f"  ✗ '{c}': forma desconhecida — use 'nome [ref] · projeto'")
            falhou = 1
            continue
        nome, ref, projeto = m.group("nome"), m.group("ref"), m.group("projeto")
        cand = [s for s in sessoes if s["nome"] == nome and (projeto is None or s["projeto"] == projeto)]
        if ref:
            alvo = [s for s in cand if s["ref"] == ref]
            if alvo and alvo[0]["viva"]:
                print(f"  ✓ '{c}' → entrega a {nome} [{ref}] · {alvo[0]['projeto']}")
            else:
                print(f"  ✗ '{c}' → RECUSADO: ref morto ou inexistente; não cai para o nome")
                falhou = 1
            continue
        vivas = [s for s in cand if s["viva"]]
        if len(vivas) == 1:
            s = vivas[0]
            print(f"  ✓ '{c}' → entrega a {s['nome']} [{s['ref']}] · {s['projeto']}")
        elif not vivas:
            print(f"  ✗ '{c}' → RECUSADO: nenhuma sessão viva com esse endereço")
            falhou = 1
        else:
            lista = ", ".join(f"[{s['ref']}] · {s['projeto']}" for s in vivas)
            print(f"  ✗ '{c}' → RECUSADO: ambíguo ({len(vivas)} sessões vivas: {lista}); diga nome [ref] · projeto")
            falhou = 1
    return falhou


# --------------------------------------------------------------------------- glossario
def sha_modelo(caminho):
    # sha256 do modelo em forma canônica (chaves ordenadas, sem espaço): a quebra de linha do
    # sistema operacional não muda o carimbo; um caractere do conteúdo muda.
    canonico = json.dumps(carregar(caminho), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonico.encode("utf-8")).hexdigest()


def gerar_glossario(caminho_modelo):
    modelo = carregar(caminho_modelo)
    out = [f"<!-- GERADO de modelo.json · sha256={sha_modelo(caminho_modelo)} · não edite à mão: edite o modelo e regere -->",
           f"# Glossário — {modelo['dominio']}", "",
           "| termo de tela | identificador | contexto | definição |", "|---|---|---|---|"]
    for t in sorted(modelo["termos"], key=lambda t: (t["contexto"], t["tela"])):
        out.append(f"| {t['tela']} | `{t['codigo']}` | {t['contexto']} | {t['definicao']} |")
    out += ["", "Nunca escrever nu:", ""]
    out += [f"- **{f}** — {regra}" for f, regra in sorted(modelo["familias"].items())]
    out += ["", "Siglas:", ""]
    out += [f"- **{s}** — {e}" for s, e in sorted(modelo["siglas"].items())]
    return "\n".join(out) + "\n"


def conferir_glossario(caminho_modelo, caminho_glossario):
    gravado = Path(caminho_glossario).read_text(encoding="utf-8")
    print(f"conferir {Path(caminho_glossario).name} contra {Path(caminho_modelo).name}")
    falhou = 0
    m = re.search(r"sha256=([0-9a-f]{64})", gravado.splitlines()[0] if gravado else "")
    atual = sha_modelo(caminho_modelo)
    if not m:
        print("  ✗ sem o carimbo do modelo: não foi gerado (ou o cabeçalho foi apagado)")
        falhou = 1
    elif m.group(1) != atual:
        print(f"  ✗ o modelo mudou depois da geração (gravado {m.group(1)[:12]}…, atual {atual[:12]}…)")
        falhou = 1
    regerado = gerar_glossario(caminho_modelo)
    a, b = gravado.splitlines(), regerado.splitlines()
    for n in range(max(len(a), len(b))):
        la = a[n] if n < len(a) else "<fim>"
        lb = b[n] if n < len(b) else "<fim>"
        if n == 0:
            continue  # o carimbo já foi conferido acima
        if la != lb:
            print(f"  ✗ linha {n + 1} difere do que o modelo gera:")
            print(f"      no arquivo: {la}")
            print(f"      do modelo : {lb}")
            falhou = 1
            break
    if not falhou:
        print("  ✓ carimbo bate e o texto regerado do modelo é idêntico, byte a byte")
    return falhou


# --------------------------------------------------------------------------- mutacao
def mutacao(modelo, base):
    casos = Path(base) / "casos"
    pares = [
        ("lint ", lambda p: len(achados_lint(modelo, p.read_text(encoding="utf-8"))), "tela-boa.md", "tela-ruim.md"),
        ("plano", lambda p: len(achados_plano(p.read_text(encoding="utf-8"))), "plan-ok.md", "plan-ruim.md"),
    ]
    todas = True
    for nome, regua, boa, ruim in pares:
        nb, nr = regua(casos / boa), regua(casos / ruim)
        ok = nb == 0 and nr > 0
        todas &= ok
        print(f"  {nome}  boa {nb} achado(s) · ruim {nr} achado(s) · discrimina: {'sim' if ok else 'NÃO'}")
    print("✓ as duas réguas discriminam." if todas else "✗ régua que não discrimina não é régua.")
    return 0 if todas else 1


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, args = argv[1], argv[2:]
    if cmd == "decidir" and len(args) == 2:
        return decidir(carregar(args[0]), carregar(args[1]))
    if cmd == "lint" and len(args) == 2:
        return lint(carregar(args[0]), args[1])
    if cmd == "plano" and len(args) == 1:
        return plano(args[0])
    if cmd == "endereco" and len(args) >= 2:
        return endereco(carregar(args[0]), args[1:])
    if cmd == "glossario" and args[:1] == ["gerar"] and len(args) == 2:
        sys.stdout.write(gerar_glossario(args[1]))
        return 0
    if cmd == "glossario" and args[:1] == ["conferir"] and len(args) == 3:
        return conferir_glossario(args[1], args[2])
    if cmd == "mutacao" and len(args) == 1:
        return mutacao(carregar(args[0]), Path(args[0]).parent)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
