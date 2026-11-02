# Inventário do capítulo C

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (5) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| LIVRO-METODO-196 | livro:maestro-handbook/receitas/instalar-o-maestro.md | Instalacao real por maestro init --ai claude escreve 81 arquivos (13 agentes, 12 comandos, 9 check-*, 6 skills, 12 templates, governanca, evals/); --ai codex escreve 53 sem .claude/. |  |
| LIVRO-METODO-286 | livro:pesquisa/base-de-pesquisa.md §No repositorio | protocol.md + runs/ com schema imutavel no repositorio. |  |
| LIVRO-METODO-289 | livro:pesquisa/base-de-pesquisa.md §No repositorio | Tags e releases reproduziveis. |  |
| GOV-174 | maestro:scripts/check-installed.sh @ 64e52a0 | check-installed.sh: instala num diretório vazio e exercita o resultado; nasceu de dois defeitos achados por agente companheiro numa instalação real (check-roles lendo arquivo não copiado; /speckit.* apontando para caminho não criado): enviávamos algo que aponta para o que não enviamos. | sim |
| GOV-178 | maestro:scripts/install-maestro.sh | install-maestro.sh: instala o método completo (agentes, skills, scripts, templates, hooks) em outro repositório; --dry-run, --ai, --write-block, --no-hooks, --force; nunca sobrescreve (salva a versão do outro). |  |

## Itens SECUNDÁRIOS (26) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-A-013 | maestro:specs/013-livro-guia-editorial-piloto/spec.md @ f9f813b | Ciclo 013: guia editorial do livro (esqueleto de 9 seções, datação de livro vivo, Iron Law editorial), capítulo-piloto de 14 decisões de engenharia e o instalador instalar-maestro.sh (não sobrescreve sem --forcar, tem --dry-run); ADR 0011. | 14 |
| DECISOES-008 | maestro:docs/adr/0011-livro-padrao-editorial-e-companion.md | ADR 0011: padrão editorial do livro (esqueleto de 9 seções com exemplo de ciclo real e verificação obrigatórios), cinco trilhas de navegação, migração gradual com capítulo 13 piloto e companion com backend. | 14 |
| DECISOES-009 | maestro:docs/adr/0012-distribuicao-em-tres-camadas.md | ADR 0012: distribuição em três camadas — install-maestro.sh (canônico), plugin do Claude Code gerado por package-plugin.sh e npx skills add; decide não construir CLI próprio. | 12 |
| DECISOES-069 | maestro:docs/records/decisoes.jsonl#achado-060-numeros-do-README-sem-portao · commit d049dd4 | Contagens do README sem portão; ids --ai errados por três ciclos; check-installed compara dez afirmações. | 10 |
| DECISOES-099 | maestro:docs/roadmap.md#F5-F6 | F5–F6: livro (9 seções, cinco trilhas) e companion, falta publicar o serviço. | 14 |
| DECISOES-108 | maestro:docs/roadmap.md#F23 | F23: check-installed.sh instala num diretório vazio e exercita o resultado. | 10 |
| DECISOES-109 | maestro:docs/roadmap.md#F26-F27 | F26–F27: instalador que atualiza por manifesto com hash e porta da frente bin/maestro init. | 12 |
| DECISOES-119 | maestro:CHANGELOG.md#0.2.0 | v0.2.0: o método verificado onde cai — 16 portões, 13 bloqueantes. | 10 |
| DECISOES-120 | maestro:CHANGELOG.md#0.3.0 | v0.3.0: porta de entrada — 17 portões, 14 bloqueantes + metade da conformidade; maestro init. | 12 |
| DECISOES-168 | maestro:docs/research/prompt-pesquisa-praticas-desenvolvimento.md | O prompt da pesquisa profunda sobre práticas humano + agentes. | 15 |
| LIVRO-METODO-177 | livro:maestro-handbook/receitas/abrir-um-ciclo.md | Receita de abrir ciclo: classificar a raia em 30 s, scripts/new-cycle.sh NNN slug cria specs/NNN-slug com os quatro artefatos sem sobrescrever. | 4 |
| LIVRO-METODO-188 | livro:maestro-handbook/receitas/instalar-o-maestro.md | Instalar nao e copiar: instalado e quando a IA sabe que deve seguir o metodo, e check-install.sh so fica verde com as duas metades. | 12 |
| LIVRO-METODO-189 | livro:maestro-handbook/receitas/instalar-o-maestro.md | Tres caminhos de distribuicao (ADR 0012): A script com o metodo inteiro, B plugin do Claude Code (agentes+skills+comandos), C npx skills add (so as 6 skills), cada um declarando o que nao leva. | 12 |
| LIVRO-METODO-190 | livro:maestro-handbook/receitas/instalar-o-maestro.md | maestro init conduz agente, destino, instalacao e verificacao e sai diferente de zero se a verificacao falhar; sem terminal e sem --yes ele recusa. | 12 |
| LIVRO-METODO-232 | maestro:docs/comece-por-aqui.md | Mapa de leitura: principios, modelo operacional, handbook e pratica pelos templates (/speckit.specify, PR template, /dod), com glossario para toda sigla. | A |
| LIVRO-METODO-248 | livro:pesquisa/base-de-pesquisa.md §Quatro corpora | Quatro corpora: metodo normativo (docs/governance), handbook do metodo por versao, livro (argumento duravel) e pesquisa (protocolo, runs, datasets, replicacao). | 15 |
| LIVRO-METODO-261 | livro:pesquisa/base-de-pesquisa.md §Agenda | Repeticoes com distribuicao e intervalo e ambiente congelado (commit, modelo, harness, hashes). | 15 |
| LIVRO-METODO-262 | livro:pesquisa/base-de-pesquisa.md §Agenda | Corpus de ciclos historicos do proprio Maestro como fonte de evidencia. | 15 |
| LIVRO-METODO-287 | livro:pesquisa/base-de-pesquisa.md §No repositorio | Gate mutation estruturado: propriedade, fixture positiva, fixture negativa, resultado esperado. | 10 |
| LIVRO-METODO-288 | livro:pesquisa/base-de-pesquisa.md §No repositorio | CLAIMS.md: nenhum numero sem claim ID. | 15 |
| GOV-151 | maestro:scripts/hooks/merge-settings.py @ 813a469 | Merge do settings.json de terceiros, nunca sobrescrito (WRITE/CURRENT/MERGED/UPGRADE/CONFLICT/ERROR); CURRENT nasceu porque o instalador conflitava consigo mesmo e UPGRADE porque projeto instalado na v0.3.0 recebia CONFLICT ao atualizar. | 12 |
| GOV-152 | maestro:scripts/README.md | Princípio dos scripts (II + III): o script faz a parte mecânica do ritual repetido e o gate fica humano; cada script nasceu de dor real em retro; os marcados '¹' não viajam com a instalação. | 3 |
| GOV-162 | maestro:scripts/check-retro.sh @ 64e52a0 | Terceira ocorrência do anti-padrão 21: sem specs/, 'ls' num pipe com pipefail e set -e matava check-retro.sh em silêncio (exit 2, sem saída) numa instalação nova; achado no ciclo 048. | 10 |
| GOV-171 | maestro:scripts/check-flags.sh @ 7bef06a | check-flags.sh: o conjunto de flags que o parser aceita é igual ao que a prosa promete, nos dois sentidos; nasceu da receita que ensinava '--forcar' (inexistente) e do cabeçalho do instalador sem --ai, --no-hooks e --write-block (ciclo 058). | 10 |
| GOV-179 | maestro:scripts/install-agents.tsv @ 17d44e8 | Tabela de agentes suportados (ciclo 057): 'a tabela É o suporte', ids na grafia do upstream; '-' em commands significa formato não verificado; a primeira versão afirmava que as quatro instruções vinham do upstream e duas não vinham (revisão independente). | 12 |
| GOV-180 | maestro:scripts/package-plugin.sh | package-plugin.sh: constrói o plugin do Claude Code a partir das fontes canônicas (.claude/agents, .claude/commands, skills/); --verify prova sincronia e bloqueia na CI. | 12 |
