#!/usr/bin/env python3
"""futuro.py — três verificações do capítulo 16, sem dependência externa.

  sensibilidade [AXIOMA ...]   quais teoremas e corolários ficam expostos (ou sem apoio)
                               se os axiomas citados enfraquecerem com a próxima geração
  gatilhos ESTADO EVENTOS      quais ideias em "observar" tiveram o gatilho disparado por um
                               evento registrado DEPOIS da data do estado, e não foram reavaliadas
  calendario DATA              o que do AI Act se aplica na data, na versão original e na alterada;
                               sai 1 se o dado passou da validade desde a última conferência
  demo                         o roteiro do capítulo (sai 0 se os resultados esperados aparecerem)

Saída: 0 = conforme · 1 = achado (gatilho disparado sem reavaliação, ou calendário vencido) · 2 = erro de uso.
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"


def carregar_json(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def carregar_jsonl(caminho):
    linhas = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                linhas.append(json.loads(linha))
    return linhas


# ---------------------------------------------------------------- 1. sensibilidade
def sensibilidade(modelo, fracos):
    """Um elemento fica EXPOSTO se alguma das suas fontes está fraca ou exposta, e SEM APOIO
    se todas as suas fontes estão fracas ou sem apoio. Axioma fraco conta como sem apoio."""
    fracos = set(fracos)
    desconhecidos = fracos - set(modelo["axiomas"])
    if desconhecidos:
        raise ValueError(f"axioma desconhecido: {sorted(desconhecidos)}")
    sem_apoio = set(fracos)
    exposto = set(fracos)
    for grupo in ("teoremas", "corolarios"):
        for nome, fontes in modelo[grupo].items():
            if any(f in exposto for f in fontes):
                exposto.add(nome)
            if all(f in sem_apoio for f in fontes):
                sem_apoio.add(nome)
    def so(grupo, conjunto):
        return [n for n in modelo[grupo] if n in conjunto]
    return {
        "teoremas_expostos": so("teoremas", exposto),
        "teoremas_sem_apoio": so("teoremas", sem_apoio),
        "corolarios_expostos": so("corolarios", exposto),
        "corolarios_sem_apoio": so("corolarios", sem_apoio),
        "teoremas_intactos": [n for n in modelo["teoremas"] if n not in exposto],
        "corolarios_intactos": [n for n in modelo["corolarios"] if n not in exposto],
    }


def imprimir_sensibilidade(modelo, fracos):
    r = sensibilidade(modelo, fracos)
    nt, nc = len(modelo["teoremas"]), len(modelo["corolarios"])
    print(f"  axiomas enfraquecidos: {', '.join(fracos) or '(nenhum)'}")
    print(f"  teoremas expostos   {len(r['teoremas_expostos'])}/{nt}: {' '.join(r['teoremas_expostos']) or '-'}")
    print(f"  teoremas sem apoio  {len(r['teoremas_sem_apoio'])}/{nt}: {' '.join(r['teoremas_sem_apoio']) or '-'}")
    print(f"  teoremas intactos   {len(r['teoremas_intactos'])}/{nt}: {' '.join(r['teoremas_intactos']) or '-'}")
    print(f"  corolários expostos {len(r['corolarios_expostos'])}/{nc}; sem apoio {len(r['corolarios_sem_apoio'])}/{nc}: {' '.join(r['corolarios_sem_apoio']) or '-'}")
    return r


# ---------------------------------------------------------------- 2. gatilhos
def estado_corrente(linhas):
    """O índice só cresce: o estado corrente de uma ideia é a sua ÚLTIMA linha."""
    atual = {}
    for o in linhas:
        atual[o["ideia"]] = o
    return atual


def gatilhos(estado_linhas, eventos):
    atual = estado_corrente(estado_linhas)
    observadas = {k: v for k, v in atual.items() if v["estado"] == "observar"}
    sem_gatilho = [k for k, v in observadas.items() if not (v.get("gatilho") or "").strip()]
    disparados = []
    for ideia, linha in observadas.items():
        posteriores = [e for e in eventos if e["ideia"] == ideia and e["data"] > linha["data"]]
        if posteriores:
            disparados.append((ideia, linha, posteriores))
    return observadas, sem_gatilho, disparados


def imprimir_gatilhos(estado_linhas, eventos):
    observadas, sem_gatilho, disparados = gatilhos(estado_linhas, eventos)
    print(f"  ideias em 'observar': {len(observadas)}")
    print(f"  portão antigo (todo 'observar' tem gatilho?): "
          f"{'VERDE' if not sem_gatilho else 'VERMELHO ' + str(sem_gatilho)}")
    if not disparados:
        print("  portão novo (algum gatilho disparou sem reavaliação?): VERDE — nenhum")
    else:
        print(f"  portão novo (algum gatilho disparou sem reavaliação?): VERMELHO — {len(disparados)}")
        for ideia, linha, evs in disparados:
            print(f"    ✗ {ideia}: estado 'observar' desde {linha['data']}; gatilho: \"{linha['gatilho']}\"")
            for e in evs:
                print(f"        disparado em {e['data']}: {e['evento']} [{e['prova']}]")
    return 1 if disparados else 0


# ---------------------------------------------------------------- 3. calendário

def calendario(dados, data):
    linhas = []
    for m in dados["marcos"]:
        orig = m["original"]
        linhas.append((m["o_que"], orig is not None and orig <= data, m["alterado"] <= data,
                       orig, m["alterado"], m["conteudo_mudou"]))
    return linhas


def frescor(dados, data):
    """A única checagem do relógio que não é circular: o dado diz QUANDO foi conferido contra
    a fonte oficial. Passado o prazo de validade, o calendário não responde: manda reconferir."""
    conferido = dados.get("conferido_em")
    if not conferido:
        return False, "sem data de conferência"
    limite = (date.fromisoformat(conferido) + timedelta(days=int(dados.get("validade_dias", 90)))).isoformat()
    if data > limite:
        return False, f"conferido em {conferido}, vencido desde {limite}: reconfira no Jornal Oficial"
    return True, f"conferido em {conferido}, válido até {limite}"


def imprimir_calendario(dados, data):
    print(f"  data consultada: {data}")
    fresco, motivo = frescor(dados, data)
    print(f"  frescor do dado: {'OK' if fresco else 'VENCIDO'} — {motivo}")
    def sim(b):
        return "aplica" if b else "ainda não"
    for o_que, orig, alt, d_orig, d_alt, mudou in calendario(dados, data):
        marca = "  " if d_orig == d_alt else "↻ "
        txt_orig = f"{d_orig} ({sim(orig)})" if d_orig else "não existia"
        print(f"  {marca}{o_que}")
        print(f"      original {txt_orig} · alterado {d_alt} ({sim(alt)}) · conteúdo mudou? {mudou}")
    alterados = [m for m in dados["marcos"] if m["original"] != m["alterado"]]
    print(f"  marcos com data alterada ou criados: {len(alterados)} de {len(dados['marcos'])}")
    return 0 if fresco else 1


# ---------------------------------------------------------------- demo
def demo():
    modelo = carregar_json(DADOS / "axiomas.json")
    estado = carregar_jsonl(DADOS / "estado.jsonl")
    eventos = carregar_jsonl(DADOS / "eventos.jsonl")
    ai_act = carregar_json(DADOS / "ai-act.json")
    ok = True

    print("1. Sensibilidade do método à próxima geração de modelos")
    print(" a) cenário 'janela maior e que não degrada' (A3 enfraquece)")
    r = imprimir_sensibilidade(modelo, ["A3"])
    ok &= r["teoremas_expostos"] == ["T2", "T5", "T6"] and r["teoremas_sem_apoio"] == []
    print(" b) cenário 'janela maior e memória persistente do fornecedor' (A3 e A4 enfraquecem)")
    r = imprimir_sensibilidade(modelo, ["A3", "A4"])
    ok &= r["teoremas_sem_apoio"] == ["T5", "T6"] and r["teoremas_intactos"] == ["T3"]
    print(" c) cenário de controle: o que nenhum modelo muda (A1, A2, A5) segue de pé")
    r = imprimir_sensibilidade(modelo, [])
    ok &= len(r["teoremas_intactos"]) == 7

    print()
    print("2. Gatilhos de reavaliação: escritos × vigiados (índice real, maestro@19823c2)")
    print(" a) o índice como está")
    codigo = imprimir_gatilhos(estado, eventos)
    ok &= codigo == 1
    print(" b) depois de anexar uma linha de reavaliação para cada ideia disparada")
    corrigido = list(estado) + [
        {"ideia": "trilha-com-custo", "estado": "absorver", "data": "2026-11-02",
         "destino": "docs/governance/task-ledger.md", "gatilho": "", "nota": "reavaliada (exemplo)"},
        {"ideia": "worktree-por-task", "estado": "observar", "data": "2026-11-02", "destino": "",
         "gatilho": "conflito entre worktrees que a integração manual não resolva", "nota": "reavaliada (exemplo)"},
    ]
    codigo = imprimir_gatilhos(corrigido, eventos)
    ok &= codigo == 0

    print()
    print("3. O relógio regulatório: AI Act")
    print(" a) em 2026-11-02")
    ok &= imprimir_calendario(ai_act, "2026-11-02") == 0
    aplica = [o for o, _, alt, *_ in calendario(ai_act, "2026-11-02") if alt]
    ok &= len(aplica) == 3
    print(" b) o mesmo dado consultado em 2027-03-01, sem nova conferência")
    fresco, motivo = frescor(ai_act, "2027-03-01")
    print(f"  frescor do dado: {'OK' if fresco else 'VENCIDO'} — {motivo}")
    ok &= not fresco

    print()
    print("roteiro:", "OK — os resultados esperados apareceram" if ok else "FALHOU — algum resultado mudou")
    return 0 if ok else 1


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    try:
        if cmd == "demo":
            return demo()
        if cmd == "sensibilidade":
            imprimir_sensibilidade(carregar_json(DADOS / "axiomas.json"), argv[2:])
            return 0
        if cmd == "gatilhos" and len(argv) == 4:
            return imprimir_gatilhos(carregar_jsonl(argv[2]), carregar_jsonl(argv[3]))
        if cmd == "calendario" and len(argv) == 3:
            return imprimir_calendario(carregar_json(DADOS / "ai-act.json"), argv[2])
    except (OSError, ValueError, KeyError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    print(__doc__)
    return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv))
