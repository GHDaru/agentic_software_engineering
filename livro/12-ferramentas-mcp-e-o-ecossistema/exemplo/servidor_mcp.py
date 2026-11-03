#!/usr/bin/env python3
"""Um servidor MCP mínimo (stdio, JSON-RPC 2.0, só biblioteca padrão), em duas versões.

    python servidor_mcp.py             # a versão GUARDADA
    python servidor_mcp.py --ingenuo   # a versão INGÊNUA: a mesma interface, sem as guardas

Três ferramentas, escolhidas porque cada uma tem um risco diferente:

    ler_doc(nome)            lê um documento de docs/  -> o risco é o CONTEÚDO que volta ao modelo
    registrar_status(texto)  acrescenta uma linha      -> o risco é QUEM assina a linha
    apagar_registro()        apaga o registro          -> o risco é a AÇÃO, irreversível

A versão guardada aplica cinco regras, todas FORA do modelo (ele só manda texto):

  1. a identidade vem do token do processo (variável SESSAO_TOKEN), nunca de argumento;
  2. a política allow/deny/ask é por papel e por ferramenta (politica.json), e `ask` não executa;
  3. a ferramenta negada nem aparece no tools/list (menor privilégio também na descoberta);
  4. o resultado volta ao modelo entre as marcas da cerca, com teto de bytes e marca de corte,
     e uma marca de cerca vinda de dentro do documento é neutralizada;
  5. ler_doc só lê dentro de docs/ (caminho resolvido, não comparado como texto).

A cerca NÃO é uma sandbox: quem lê ainda pode obedecer ao que está dentro. Ela torna visível
onde o dado de terceiros começa e termina. Quem impede a ação é a regra 2.

Os tokens e o "segredo" deste diretório são de demonstração; não há nada real aqui.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(AQUI, "docs")
INGENUO = "--ingenuo" in sys.argv[1:]

LIMITE = 512  # bytes que o resultado de uma ferramenta pode ocupar no contexto do modelo
CERCA_ABRE = "<<<DADO-DE-TERCEIROS>>>"
CERCA_FECHA = "<<<FIM-DO-DADO>>>"
MARCA_CORTE = "\n[truncado: o dado passou do teto do contexto]"

FERRAMENTAS = {
    "ler_doc": {
        "description": "Lê um documento da pasta docs/ do projeto.",
        "inputSchema": {"type": "object", "required": ["nome"],
                        "properties": {"nome": {"type": "string"}}},
    },
    "registrar_status": {
        "description": "Acrescenta uma linha de status ao registro. A identidade vem do token.",
        # A versão guardada NÃO declara 'autor': quem chama não diz quem é.
        "inputSchema": {"type": "object", "required": ["texto"],
                        "properties": {"texto": {"type": "string"}}},
    },
    "apagar_registro": {
        "description": "Apaga o registro inteiro. Irreversível.",
        "inputSchema": {"type": "object", "properties": {}},
    },
}


def carrega(nome):
    with open(os.path.join(AQUI, nome), encoding="utf-8") as f:
        return json.load(f)


POLITICA = carrega("politica.json")
SESSOES = carrega("sessoes.json")  # sha256(token) -> {endereco, papel}; o token não fica no disco
REGISTRO: list[dict] = []


def quem_sou():
    """A identidade pelo token do processo. Sem token conhecido, não há identidade."""
    token = os.environ.get("SESSAO_TOKEN", "")
    return SESSOES.get(hashlib.sha256(token.encode("utf-8")).hexdigest())


class Recusa(Exception):
    pass


def decisao(papel, ferramenta):
    return POLITICA.get(papel, {}).get(ferramenta, "deny")  # o que não está escrito é negado


def cercado(texto: str) -> str:
    """O dado entre as marcas, com teto para o conjunto e marca de corte quando cortou."""
    miolo = texto.replace(CERCA_ABRE, "[cerca neutralizada]").replace(CERCA_FECHA, "[cerca neutralizada]")
    abre, fecha = (CERCA_ABRE + "\n").encode(), ("\n" + CERCA_FECHA).encode()
    cru = miolo.encode("utf-8")
    if len(abre) + len(cru) + len(fecha) > LIMITE:
        sobra = LIMITE - len(abre) - len(fecha) - len(MARCA_CORTE.encode("utf-8"))
        cru = cru[:sobra].decode("utf-8", errors="ignore").encode("utf-8") + MARCA_CORTE.encode("utf-8")
    return (abre + cru + fecha).decode("utf-8")


def ler_doc(nome: str) -> str:
    if INGENUO:
        with open(os.path.join(DOCS, nome), encoding="utf-8") as f:
            return f.read()
    alvo = os.path.realpath(os.path.join(DOCS, nome))
    if os.path.commonpath([alvo, os.path.realpath(DOCS)]) != os.path.realpath(DOCS):
        raise Recusa(f"fora de docs/: {nome!r}")
    with open(alvo, encoding="utf-8") as f:
        return cercado(f.read())


def chama(nome, args):
    if nome not in FERRAMENTAS:
        raise Recusa(f"ferramenta inexistente: {nome}")
    if INGENUO:
        eu = {"endereco": args.get("autor", "anonimo"), "papel": "?"}
    else:
        eu = quem_sou()
        if eu is None:
            raise Recusa("sem identidade: o token desta sessão não está registrado")
        d = decisao(eu["papel"], nome)
        if d == "deny":
            raise Recusa(f"negado pela política: o papel '{eu['papel']}' não chama '{nome}'")
        if d == "ask":
            raise Recusa(f"pede aprovação humana: '{nome}' é classe irreversível para '{eu['papel']}'; nada foi executado")
    if nome == "ler_doc":
        return ler_doc(str(args.get("nome", "")))
    if nome == "registrar_status":
        linha = {"autor": eu["endereco"], "texto": str(args.get("texto", ""))}
        if not INGENUO and args.get("autor") not in (None, eu["endereco"]):
            linha["ignorado"] = {"autor": args["autor"]}
        REGISTRO.append(linha)
        return json.dumps(linha, ensure_ascii=False)
    n = len(REGISTRO)
    REGISTRO.clear()
    return f"registro apagado ({n} linhas)"


def responde(req):
    m = req.get("method")
    if m == "initialize":
        return {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}},
                "serverInfo": {"name": "exemplo-cap12", "version": "1.0"}}
    if m == "tools/list":
        if INGENUO:
            nomes = list(FERRAMENTAS)
        else:
            eu = quem_sou()
            nomes = [] if eu is None else [n for n in FERRAMENTAS if decisao(eu["papel"], n) != "deny"]
        return {"tools": [{"name": n, **FERRAMENTAS[n]} for n in nomes]}
    if m == "tools/call":
        p = req.get("params", {})
        try:
            texto = chama(p.get("name"), p.get("arguments") or {})
        except (Recusa, OSError) as e:
            return {"content": [{"type": "text", "text": f"recusado: {e}"}], "isError": True}
        return {"content": [{"type": "text", "text": texto}]}
    raise LookupError(m)


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    for linha in sys.stdin:
        if not linha.strip():
            continue
        req = json.loads(linha)
        if req.get("id") is None:  # notificação: não tem resposta
            continue
        try:
            out = {"jsonrpc": "2.0", "id": req["id"], "result": responde(req)}
        except LookupError as e:
            out = {"jsonrpc": "2.0", "id": req["id"],
                   "error": {"code": -32601, "message": f"método desconhecido: {e}"}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
