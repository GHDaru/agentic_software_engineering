#!/usr/bin/env python3
"""contexto.py — as quatro operações da engenharia de contexto, medidas num projeto de brinquedo.

Capítulo 5 do livro "Engenharia de Software Orientada por Agentes". Só biblioteca padrão.

Subcomandos (cada um imprime o que mediu e sai 0 = conforme, 1 = achado, 2 = uso errado):

  selecionar  <projeto> <ciclo> <tarefa>     seleção: o que a tarefa precisa × o repositório inteiro
  compactar   <projeto> <ciclo> [--tasks F] [--conversa F]
                                             compressão: o que sobrevive quando só o tasks.md fica
  registrar   <arquivo.jsonl> '<json>'       persistência: acrescenta uma decisão, validando
  historico   <antes.jsonl> <depois.jsonl>   persistência: o depois é o antes + acréscimos?
  transferir  <projeto> [--corrigir]         transferência: a instrução que a IA lê bate com o disco?
  rastrear    <projeto> <id-do-gate>         rastreabilidade: do gate até o porquê, de trás para frente
  inspecionar <projeto> <ciclo>              as quatro operações num quadro só

Tokens são ESTIMADOS: caracteres / 4, arredondado para cima. É uma régua grosseira e
declarada; o que importa aqui é a razão entre selecionado e total, não o valor absoluto.
"""
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

OK, ACHADO, USO = 0, 1, 2


def tokens(texto):
    return (len(texto) + 3) // 4


def ler(p):
    return Path(p).read_text(encoding="utf-8")


def pasta_do_ciclo(projeto, ciclo):
    achados = sorted((Path(projeto) / "specs").glob(f"{ciclo}-*"))
    if not achados:
        sys.exit(f"✗ ciclo {ciclo} não existe em {projeto}/specs")
    return achados[0]


def tarefas(texto):
    """{'T1': 'linha inteira', ...} a partir de linhas '- [ ] **Tn** — ...'."""
    return {m.group(1): m.group(0) for m in re.finditer(r"^- \[[ x]\] \*\*(T\d+)\*\*.*$", texto, re.M)}


# ── seleção ──────────────────────────────────────────────────────────────────────────────

def arquivos_de_texto(projeto):
    for p in sorted(Path(projeto).rglob("*")):
        if p.is_file() and p.suffix in {".md", ".py", ".jsonl", ".txt"}:
            yield p


def medir_selecao(projeto, ciclo, tarefa):
    projeto = Path(projeto)
    pasta = pasta_do_ciclo(projeto, ciclo)
    linhas = tarefas(ler(pasta / "tasks.md"))
    if tarefa not in linhas:
        sys.exit(f"✗ {tarefa} não está em {pasta.name}/tasks.md")
    linha = linhas[tarefa]
    total = sum(tokens(ler(p)) for p in arquivos_de_texto(projeto))
    itens = [("spec.md (contexto integrador)", tokens(ler(pasta / "spec.md"))),
             (f"{tarefa} (a linha da tarefa)", tokens(linha))]
    citados = re.findall(r"`(src/[^`]+)`", linha)
    for c in citados:
        itens.append((c, tokens(ler(projeto / c))))
    selecionado = sum(t for _, t in itens)
    return linha, itens, citados, selecionado, total


def cmd_selecionar(projeto, ciclo, tarefa):
    linha, itens, citados, sel, total = medir_selecao(projeto, ciclo, tarefa)
    print(f"seleção {ciclo}/{tarefa}")
    for nome, t in itens:
        print(f"  + {nome:<34} {t:>5} tokens")
    economia = 100 * (total - sel) // total
    print(f"  selecionado {sel} de {total} tokens do repositório inteiro → economia {economia}%")
    if not citados:
        print("✗ a tarefa não cita arquivo: quem a executa vai procurar o contexto sozinho (ou na conversa).")
        return ACHADO
    if economia < 50:
        print("✗ economia baixa: a tarefa atravessa fronteiras. Reveja o corte; não aumente a janela.")
        return ACHADO
    print("✓ corte por fronteira: a tarefa cabe no que ela mesma declara.")
    return OK


# ── compressão ───────────────────────────────────────────────────────────────────────────

# (nome, onde procurar ANTES da compactação, o que precisa estar no tasks.md DEPOIS)
FATOS = [
    ("revisão em contexto fresco", r"revisão independente|contexto fresco", r"TAIL:review"),
    ("revisão de segurança", r"segurança", r"TAIL:security"),
    ("gate humano antes do merge", r"gate humano|meu gate", r"TAIL:gate"),
    ("data dd/mm/aaaa na mensagem", r"dd/mm/aaaa", r"dd/mm/aaaa"),
]


def sem_contexto(linha):
    """Tarefa autossuficiente: cita um arquivo ou comando (`...`) E tem critério (→)."""
    return "`" in linha and "→" in linha


def cmd_compactar(projeto, ciclo, tasks_arq=None, conversa_arq=None):
    pasta = pasta_do_ciclo(projeto, ciclo)
    tasks_p = Path(tasks_arq) if tasks_arq else pasta / "tasks.md"
    fontes = {"spec.md": ler(pasta / "spec.md"), "plan.md": ler(pasta / "plan.md"),
              tasks_p.name: ler(tasks_p)}
    if conversa_arq:
        fontes["conversa"] = ler(conversa_arq)
    antes = sum(tokens(t) for t in fontes.values())
    depois_txt = fontes[tasks_p.name]
    print(f"compactação {ciclo}: janela com {', '.join(fontes)} ({antes} tokens)")
    print(f"  → depois: só o que o executor segue, {tasks_p.name} ({tokens(depois_txt)} tokens)")
    falhas = 0
    for nome, re_antes, re_depois in FATOS:
        onde = [f for f, t in fontes.items() if f != tasks_p.name and re.search(re_antes, t, re.I)]
        if re.search(re_depois, depois_txt):
            print(f"  ✓ {nome:<30} sobrevive (está em {tasks_p.name})")
        else:
            falhas += 1
            print(f"  ✗ {nome:<30} APAGADO (estava em: {', '.join(onde) or 'lugar nenhum'})")
    dependentes = [t for t, l in tarefas(depois_txt).items() if not sem_contexto(l)]
    for t in dependentes:
        print(f"  ✗ {t} não se executa com contexto zero (sem arquivo/comando e critério →)")
    if falhas or dependentes:
        print(f"✗ {falhas} fato(s) apagado(s), {len(dependentes)} tarefa(s) presa(s) à conversa. "
              "O executor vai obedecer, com fidelidade, a versão truncada.")
        return ACHADO
    print("✓ tudo o que importa está no artefato consumido: a compactação não apaga nada que conte.")
    return OK


# ── persistência ─────────────────────────────────────────────────────────────────────────

CAMPOS = ("id", "data", "titulo", "status", "registro")


def cmd_registrar(arquivo, linha_json):
    arquivo = Path(arquivo)
    try:
        nova = json.loads(linha_json)
    except ValueError:
        print("✗ recusado: não é JSON válido.")
        return ACHADO
    faltam = [c for c in CAMPOS if not nova.get(c)]
    if faltam:
        print(f"✗ recusado: faltam os campos {', '.join(faltam)}.")
        return ACHADO
    if re.search(r"<[^>]*pendente[^>]*>|TODO", str(nova["registro"]), re.I):
        print(f"✗ recusado: o registro aponta um marcador ({nova['registro']}), não uma evidência.")
        return ACHADO
    existentes = [json.loads(l) for l in ler(arquivo).splitlines() if l.strip()]
    if any(e["id"] == nova["id"] for e in existentes):
        print(f"✗ recusado: o id {nova['id']} já existe. Corrigir é acrescentar uma linha nova "
              "com outro id (e o campo \"fecha\"), nunca reescrever.")
        return ACHADO
    if "fecha" in nova and not any(e["id"] == nova["fecha"] for e in existentes):
        print(f"✗ recusado: \"fecha\" aponta {nova['fecha']}, que nunca foi aberto.")
        return ACHADO
    with arquivo.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(nova, ensure_ascii=False) + "\n")
    print(f"✓ acrescentada como linha {len(existentes) + 1}: {nova['id']}")
    return OK


def cmd_historico(antes, depois):
    a = ler(antes).splitlines()
    d = ler(depois).splitlines()
    print(f"histórico: {Path(antes).name} ({len(a)} linhas) → {Path(depois).name} ({len(d)} linhas)")
    for i, linha in enumerate(a, 1):
        if i > len(d) or d[i - 1] != linha:
            print(f"✗ linha {i} foi reescrita ou apagada: {json.loads(linha)['id']}")
            print("  o que se pensava antes deixou de existir; a próxima sessão lê a versão nova como se sempre tivesse sido assim.")
            return ACHADO
    print(f"✓ só acréscimo: {len(d) - len(a)} linha(s) nova(s), nenhuma antiga tocada.")
    return OK


# ── transferência ────────────────────────────────────────────────────────────────────────

def skills_do_disco(projeto):
    out = []
    for s in sorted((Path(projeto) / "skills").glob("*/SKILL.md")):
        m = re.search(r"^description:\s*(.+)$", ler(s), re.M)
        primeira = re.split(r"(?<=\.)\s", m.group(1).strip())[0] if m else ""
        out.append((s.parent.name, primeira))
    return out


def conferir_instrucao(projeto):
    projeto = Path(projeto)
    skills = skills_do_disco(projeto)
    achados = []
    print(f"  skills no disco: {', '.join(n for n, _ in skills)}")
    for nome in ("CLAUDE.md", "AGENTS.md"):
        p = projeto / nome
        if not p.exists():
            continue
        txt = ler(p)
        invisiveis = [n for n, _ in skills if f"`{n}`" not in txt]
        sem_regra = "skills primeiro" not in txt.lower()
        marca = "✗" if invisiveis or sem_regra else "✓"
        detalhe = []
        if invisiveis:
            detalhe.append("não cita " + ", ".join(invisiveis))
        if sem_regra:
            detalhe.append("sem a regra 'skills primeiro'")
        print(f"  {marca} {nome:<10} {'; '.join(detalhe) or 'cita toda skill e manda consultá-las'}")
        achados += [f"{nome}: {d}" for d in detalhe]
    c, a = projeto / "CLAUDE.md", projeto / "AGENTS.md"
    if c.exists() and a.exists():
        if ler(c) == ler(a):
            print("  ✓ CLAUDE.md e AGENTS.md: mesmo conteúdo (fonte única)")
        else:
            print("  ✗ CLAUDE.md e AGENTS.md divergem: duas cópias escritas à mão")
            achados.append("duas cópias divergentes")
    return achados


def cmd_transferir(projeto, corrigir=False):
    if not corrigir:
        print(f"transferência: a instrução que a IA lê × o disco ({Path(projeto).name})")
        achados = conferir_instrucao(projeto)
        if achados:
            print(f"✗ {len(achados)} deriva(s): a IA segue menos método do que o repositório declara.")
            return ACHADO
        print("✓ instrução coerente com o disco.")
        return OK
    tmp = Path(tempfile.mkdtemp(prefix="contexto-"))
    try:
        alvo = tmp / Path(projeto).name
        shutil.copytree(projeto, alvo)
        bloco = "\n".join(f"- `{n}` — {d}" for n, d in skills_do_disco(alvo))
        c = alvo / "CLAUDE.md"
        txt = re.sub(r"(<!-- BLOCO-SKILLS:INICIO -->\n).*?(<!-- BLOCO-SKILLS:FIM -->)",
                     lambda m: m.group(1) + bloco + "\n" + m.group(2), ler(c), flags=re.S)
        c.write_text(txt, encoding="utf-8", newline="\n")
        a = alvo / "AGENTS.md"
        a.unlink()
        try:
            os.symlink("CLAUDE.md", a)          # a correção do ADR 0013 do Maestro
        except OSError:
            shutil.copyfile(c, a)               # sem permissão de symlink (Windows): cópia gerada
        print("transferência corrigida (numa cópia temporária do projeto):")
        print("  bloco de skills GERADO do disco:")
        for l in bloco.splitlines():
            print(f"    {l}")
        print("  AGENTS.md passa a ter o conteúdo de CLAUDE.md")
        achados = conferir_instrucao(alvo)
        print("✗ ainda há deriva." if achados else
              "✓ instrução coerente: skill nova sem entrada na instrução passa a ser impossível.")
        return ACHADO if achados else OK
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ── rastreabilidade ──────────────────────────────────────────────────────────────────────

CITA = re.compile(r"ciclo (\d{3})|ADR (\d{4})", re.I)


def cmd_rastrear(projeto, gate_id):
    projeto = Path(projeto)
    regs = {json.loads(l)["id"]: json.loads(l) for l in ler(projeto / "registros/decisoes.jsonl").splitlines() if l.strip()}
    commits = dict(l.split(" ", 1) for l in ler(projeto / "registros/commits.txt").splitlines() if l.strip())
    print(f"rastreio, de trás para frente, a partir de {gate_id}")
    g = regs.get(gate_id)
    if not g:
        print(f"✗ {gate_id} não está no índice de decisões")
        return ACHADO
    sha = g["registro"].split()[-1]
    print(f"  1. índice     {g['id']} ({g['data']}) → {g['registro']}")
    assunto = commits.get(sha)
    if not assunto:
        print(f"✗ o commit {sha} não existe no histórico")
        return ACHADO
    print(f"  2. commit     {sha} {assunto}")
    ciclos = [m.group(1) for m in CITA.finditer(assunto) if m.group(1)]
    adrs = [m.group(2) for m in CITA.finditer(assunto) if m.group(2)]
    if not ciclos:
        print("✗ o commit não cita ciclo: o elo se perdeu aqui")
        return ACHADO
    pasta = pasta_do_ciclo(projeto, ciclos[0])
    artefatos = [n for n in ("spec.md", "plan.md", "tasks.md", "qa-report.md") if (pasta / n).exists()]
    print(f"  3. ciclo      specs/{pasta.name}/ ({' · '.join(artefatos)})")
    for n in adrs:
        adr = sorted((projeto / "docs/adr").glob(f"{n}-*.md"))
        print(f"  4. porquê     docs/adr/{adr[0].name}" if adr else f"✗ ADR {n} citado e inexistente")
    sem = [f"{s} {a}" for s, a in commits.items() if not CITA.search(a)]
    print(f"  elos: {len(commits) - len(sem)} de {len(commits)} commits citam ciclo ou ADR")
    for s in sem:
        print(f"  ✗ sem citação: {s}  (de onde veio? só a memória de alguém sabe)")
    if sem:
        return ACHADO
    print("✓ toda mudança aponta o seu porquê.")
    return OK


# ── o quadro ─────────────────────────────────────────────────────────────────────────────

def cmd_inspecionar(projeto, ciclo):
    """Uma linha por operação, sem os detalhes: o que um 'inspect-context <ciclo>' mostraria."""
    import io
    import contextlib
    pasta = pasta_do_ciclo(projeto, ciclo)
    print(f"inspeção de contexto do ciclo {pasta.name}")
    for t in tarefas(ler(pasta / "tasks.md")):
        linha, _, citados, sel, total = medir_selecao(projeto, ciclo, t)
        eco = 100 * (total - sel) // total
        nota = "presa à conversa" if not sem_contexto(linha) else ("corte errado?" if eco < 50 else "ok")
        print(f"  seleção       {t}: {sel:>5}/{total} tokens, economia {eco:>2}%  {nota}")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r_comp = cmd_compactar(projeto, ciclo)
        r_trans = cmd_transferir(projeto)
        r_rast = cmd_rastrear(projeto, f"gate-main-{ultimo_gate(projeto)}")
    apagados = buf.getvalue().count("APAGADO")
    print(f"  compressão    {apagados} fato(s) apagado(s) se a janela compactar agora" + ("  ✗" if r_comp else "  ✓"))
    regs = [l for l in ler(Path(projeto) / "registros/decisoes.jsonl").splitlines() if l.strip()]
    print(f"  persistência  {len(regs)} decisão(ões) no índice; a última: {json.loads(regs[-1])['id']}")
    print(f"  transferência {'deriva na instrução  ✗' if r_trans else 'instrução coerente  ✓'}")
    print(f"  rastreio      {'há commit sem citação  ✗' if r_rast else 'todo commit cita o seu porquê  ✓'}")
    return ACHADO if (r_comp or r_trans or r_rast) else OK


def ultimo_gate(projeto):
    regs = [json.loads(l) for l in ler(Path(projeto) / "registros/decisoes.jsonl").splitlines() if l.strip()]
    gates = [r["id"] for r in regs if r["id"].startswith("gate-main-")]
    return gates[-1].replace("gate-main-", "") if gates else "?"


def main(argv):
    if not argv:
        print(__doc__)
        return USO
    cmd, args = argv[0], argv[1:]
    opc = {}
    pos = []
    i = 0
    while i < len(args):
        if args[i] in ("--tasks", "--conversa"):
            opc[args[i][2:]] = args[i + 1]
            i += 2
        else:
            pos.append(args[i])
            i += 1
    try:
        if cmd == "selecionar":
            return cmd_selecionar(*pos)
        if cmd == "compactar":
            return cmd_compactar(pos[0], pos[1], opc.get("tasks"), opc.get("conversa"))
        if cmd == "registrar":
            return cmd_registrar(*pos)
        if cmd == "historico":
            return cmd_historico(*pos)
        if cmd == "transferir":
            return cmd_transferir(pos[0], corrigir="--corrigir" in pos[1:])
        if cmd == "rastrear":
            return cmd_rastrear(*pos)
        if cmd == "inspecionar":
            return cmd_inspecionar(*pos)
    except TypeError:
        pass
    print(__doc__)
    return USO


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
