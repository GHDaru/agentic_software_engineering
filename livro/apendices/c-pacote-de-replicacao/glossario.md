# Glossário do apêndice C

| termo | definição |
|---|---|
| pacote de replicação | O conjunto que permite a alguém de fora reproduzir ou refutar as afirmações do livro: método instalável, versão congelada, hipóteses e protocolo, dados dos *runs* e claims com evidência. |
| claim | Afirmação quantitativa ou factual do texto com um id (`CLAIM-NN-NNN`), registrada no `claims.md` do capítulo com estado e evidência reproduzível. |
| estado do claim | Quanto a afirmação aguenta: `medido` (um comando produz o número), `observado` (um arquivo ou *commit* registra o fato), `observado (autodeclarado)` (balanço escrito pelo autor) ou `hipótese`. |
| *commit* de referência | O *commit* `19823c2` do Maestro, contra o qual todo link e toda evidência do livro são lidos; rodar em outro *commit* mede outra coisa. |
| *run* | Uma execução de um braço do experimento num cenário, registrada num diretório de `pesquisa/runs/` com `run.json` de *schema* imutável. |
| braço | Uma das condições comparadas pela agenda: A (prompt), B (spec), C (spec + portões) e T (Maestro completo). |
| célula | A combinação de braço, cenário e modelo que recebe as repetições do protocolo. |
| ambiente congelado | Os campos que tornam um *run* refazível: *commit* do método, *commit* do cenário, modelo resolvido, versão do *harness* e *hashes*. |
| protocolo | O documento que fixa, antes do primeiro dado, repetições, métricas, margens e intervalos; mudar depois de ver o resultado invalida a comparação. |
| instalador | `scripts/install-maestro.sh`: escreve o método em outro repositório sem sobrescrever o que o usuário alterou (`*.maestro-new`, `*.maestro-old`). |
| cópia instalada | O método como chega ao repositório de destino, que pode diferir da fonte; é o que `check-installed.sh` exercita num diretório vazio. |
| *release* | Versão numerada e etiquetada do método (por exemplo, 0.3.0), que comunica o que mudou; no Maestro, até 02/11/2026, existe só como seção do `CHANGELOG.md`. |
| minimização | Princípio de coletar só o necessário: a telemetria do pacote guarda contagens e rastros revisados, não o log bruto que descreve a máquina. |
| reproduzir × replicar | Na terminologia da avaliação de artefatos da ACM (versão 1.1): reproduzir é outro time obter o resultado com os artefatos do autor; replicar é obtê-lo sem eles, refazendo o experimento a partir da descrição. |
| pré-registro | Registro datado da hipótese, do desenho e da análise antes de qualquer dado, para que nada disso mude depois de ver o resultado. |
| *hash* (SHA-256) | Impressão digital de um arquivo calculada pelo Secure Hash Algorithm de 256 bits: mudou um byte, mudou o *hash*; congela a entrada de um *run*. |
| `modelo_nao_verificado` | Marca de um *run* cujo *harness* não relatou o modelo resolvido, só o apelido pedido; o *run* entra na análise com a marca. |
| *commit* não publicado | *Commit* que existe só no clone do autor; enquanto não chega ao repositório público, a evidência ancorada nele só se confere na máquina de quem o escreveu. |

