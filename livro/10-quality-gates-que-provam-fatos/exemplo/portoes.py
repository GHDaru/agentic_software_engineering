"""Seis portões para três propriedades: em cada par, um mede o PROXY e o outro mede o FATO.

Cada portão é uma função pura: recebe o texto que inspeciona e devolve True (verde) ou
False (vermelho). As três propriedades reproduzem, em miniatura, três falhas reais do
Maestro (ver ../capitulo.md, seção "A falha real" e "Teoria"):

  P1  a evidência de uma revisão registra uma revisão que ACONTECEU
      (ciclo 063: o portão aceitou "pendente." como evidência e imprimiu ✓)
  P2  a página declara o número certo de fontes
      (ciclo 016: `grep -c "https://"` contou LINHAS e reportou 5 onde havia 6)
  P3  o aviso de limiar mostra a porcentagem certa
      (ciclo 076, T045: a régua cobrava a palavra "limite" e deixou passar "9446 %")

Nenhum portão aqui sabe que está sendo testado: quem os põe à prova é provar.py.
"""
import re

# ---------------------------------------------------------------------------
# P1 — evidência de revisão
# ---------------------------------------------------------------------------

def evidencia_ingenua(linha: str) -> bool:
    """Proxy: 'o token aparece, e o que vem depois não é o marcador do gerador de ciclo'.

    É a forma do is_placeholder() antes do ciclo 063 (reconhece vazio, '<...>' e '[...]'),
    lendo o token em qualquer posição da linha (o defeito que o ciclo 055 ancorou).
    Qualquer frase escrita por gente passa, inclusive a que diz 'isto não foi feito'.
    """
    m = re.search(r"TAIL:review\s*[—:-]?\s*(.*)$", linha)
    if not m:
        return False
    valor = m.group(1).strip()
    return not (valor == "" or valor.startswith("<") or valor.startswith("["))


# Vocabulário FECHADO de ausência declarada, nos dois idiomas (o desenho do ciclo 063).
_AUSENCIA = re.compile(
    r"^[\s>(*_`\-]*(ainda\s+)?(pendente|a\s+fazer|aguardando|n[aã]o\s+executad[ao]s?|"
    r"todo|tbd|pending|not\s+run|n/d)\b",
    re.IGNORECASE,
)


def evidencia_fato(linha: str) -> bool:
    """Fato: a linha é a da cauda, tem valor, e o valor não COMEÇA declarando ausência.

    Lido do início, nunca de qualquer posição: uma evidência legítima que menciona
    'pendente' no meio de uma frase tem de continuar passando.
    """
    m = re.match(r"^\s*-\s*\[x\]\s*TAIL:review\s*[—:-]\s*(.*)$", linha, re.IGNORECASE)
    if not m:
        return False  # não achei a linha: 'não olhei' não pode ler como 'limpo'
    valor = m.group(1).strip()
    if valor == "" or valor.startswith("<") or valor.startswith("["):
        return False
    return not _AUSENCIA.match(valor)


# ---------------------------------------------------------------------------
# P2 — contagem de fontes
# ---------------------------------------------------------------------------

def _declarado(pagina: str) -> int:
    m = re.search(r"Fontes:\s*(\d+)", pagina)
    return int(m.group(1)) if m else -1


def fontes_ingenua(pagina: str) -> bool:
    """Proxy: conta LINHAS que contêm https:// (o grep -c do ciclo 016)."""
    linhas = sum(1 for l in pagina.splitlines() if "https://" in l and not l.startswith("Fontes:"))
    return linhas == _declarado(pagina)


def fontes_fato(pagina: str) -> bool:
    """Fato: conta URLs, quantas houver por linha, e exige que a página declare um número."""
    corpo = "\n".join(l for l in pagina.splitlines() if not l.startswith("Fontes:"))
    urls = re.findall(r"https://[^\s)>\]]+", corpo)
    return _declarado(pagina) >= 0 and len(urls) == _declarado(pagina)


# ---------------------------------------------------------------------------
# P3 — aviso de limiar
# ---------------------------------------------------------------------------

def limiar_ingenua(aviso: str, consumo: float) -> bool:
    """Proxy: o aviso fala de limite (a régua do jsdom da T045, antes da correção)."""
    return "limite" in aviso.lower()


def limiar_fato(aviso: str, consumo: float) -> bool:
    """Fato: o aviso afirma o número certo, com uma casa e vírgula decimal."""
    esperado = f"{consumo * 100:.1f}".replace(".", ",") + " %"
    return esperado in aviso and "limite" in aviso.lower()


PORTOES = {
    "P1": {"ingenua": evidencia_ingenua, "fato": evidencia_fato},
    "P2": {"ingenua": fontes_ingenua, "fato": fontes_fato},
    "P3": {"ingenua": limiar_ingenua, "fato": limiar_fato},
}
