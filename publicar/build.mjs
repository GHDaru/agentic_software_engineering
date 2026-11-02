// Motor do livro — Markdown (livro/) -> site estático (docs/) para o GitHub Pages
// ("Deploy from branch": main, pasta /docs).
// Adaptado do motor do Maestro (maestro-handbook/publicar/build.mjs): markdown-it como
// biblioteca, o motor é nosso. A fonte é única (o Markdown + livro/sumario.yaml); o site é
// um adapter sobre ela.
// Uso: cd publicar && npm install && npm run build      (ou: node publicar/build.mjs)

import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync, readdirSync, rmSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";
import path from "node:path";
import { fileURLToPath } from "node:url";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";
import yaml from "js-yaml";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const SAIDA = resolve(RAIZ, "docs");
const REPO = "https://github.com/GHDaru/agentic_software_engineering";
const BLOB = `${REPO}/blob/main/`;
const TREE = `${REPO}/tree/main/`;

const S = yaml.load(readFileSync(resolve(RAIZ, "livro/sumario.yaml"), "utf8"));
const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const dois = (n) => String(n).padStart(2, "0");
const decod = (s) => { try { return decodeURIComponent(s); } catch { return s; } };
const falhas = [];
const falhar = (msg) => falhas.push(msg);
const jaReprovados = new Set(); // "pagina|url" já reportado na origem: a rede de segurança não repete
const reprovar = (env, msg, url) => { falhar(`${env.fonte}: ${msg} -> ${url}`); jaReprovados.add(`${env.arquivo}|${url}`); return url; };

// Existência com a CAIXA exata: o Windows acha "Capitulo.md" quando o arquivo é
// "capitulo.md"; o GitHub Pages não. Sem isto o build fica verde e o link quebra no ar.
function existeExato(rel) {
  let atual = RAIZ;
  for (const seg of rel.split("/").filter(Boolean)) {
    let nomes;
    try { nomes = readdirSync(atual); } catch { return false; }
    if (!nomes.includes(seg)) return false;
    atual = resolve(atual, seg);
  }
  return true;
}
const ehDir = (rel) => { try { return statSync(resolve(RAIZ, rel)).isDirectory(); } catch { return false; } };

// ---------------------------------------------------------------------------
// Catálogo: a ordem de leitura vem de livro/sumario.yaml e de mais nada.
// Capítulo sem capitulo.md fica "em escrita" (aparece no sumário, sem link).
// Página opcional (exemplo, glossário, evidências) só entra se o arquivo existir.
// ---------------------------------------------------------------------------
const SLUG_OK = /^[a-z0-9-]+(\/[a-z0-9-]+)?$/;
const entradas = [];
function add(e, opcional = false) {
  e.publicada = existeExato(e.fonte);
  if (opcional && !e.publicada) return;
  entradas.push(e);
}
// Título com vírgula sem aspas dentro de {...} vira chave nula e o título sai truncado.
const conferirChaves = (e, permitidas, onde) => {
  for (const [k, v] of Object.entries(e || {}))
    if (!permitidas.includes(k) || v == null) falhar(`sumario.yaml: ${onde}: chave '${k}' ${v == null ? "vazia" : "desconhecida"} (título com vírgula precisa de aspas)`);
};
function slugValido(slug, onde) {
  if (!SLUG_OK.test(String(slug))) { falhar(`sumario.yaml: slug inválido em ${onde}: "${slug}"`); return false; }
  return true;
}

conferirChaves(S.prefacio, ["slug", "titulo"], "prefacio");
for (const p of S.partes || []) for (const c of p.capitulos || []) conferirChaves(c, ["n", "slug", "titulo", "deriva"], `capítulo ${c.n}`);
for (const a of S.apendices || []) conferirChaves(a, ["letra", "slug", "titulo"], `apêndice ${a.letra}`);
if (S.prefacio && slugValido(S.prefacio.slug, "prefacio")) {
  add({ fonte: `livro/${S.prefacio.slug}/capitulo.md`, arquivo: `${S.prefacio.slug}.html`, titulo: S.prefacio.titulo,
        rotulo: "Prefácio", grupo: "Abertura" });
}
for (const parte of S.partes || []) {
  for (const c of parte.capitulos || []) {
    if (!slugValido(c.slug, `capítulo ${c.n}`)) continue;
    add({ fonte: `livro/${c.slug}/capitulo.md`, arquivo: `${c.slug}.html`, titulo: `${dois(c.n)} — ${c.titulo}`,
          rotulo: `${c.n}. ${c.titulo}`, grupo: parte.nome, cap: c });
    add({ fonte: `livro/${c.slug}/exemplo/README.md`, arquivo: `${c.slug}-exemplo.html`,
          titulo: `Exemplo executável — ${dois(c.n)} ${c.titulo}`, rotulo: "Exemplo executável", grupo: parte.nome, filho: true }, true);
  }
}
for (const a of S.apendices || []) {
  if (!slugValido(a.slug, `apêndice ${a.letra}`)) continue;
  add({ fonte: `livro/${a.slug}/capitulo.md`, arquivo: `apendice-${path.posix.basename(a.slug)}.html`,
        titulo: `Apêndice ${a.letra} — ${a.titulo}`, rotulo: `${a.letra}. ${a.titulo}`, grupo: "Apêndices" });
}
add({ fonte: "livro/glossario.md", arquivo: "glossario.html", titulo: "Glossário", rotulo: "Glossário", grupo: "Consulta" }, true);
add({ fonte: "pesquisa/CLAIMS.md", arquivo: "evidencias.html", titulo: "Evidências (claims)", rotulo: "Evidências (claims)", grupo: "Consulta" }, true);

// Colisão de nome de página = uma sobrescreve a outra em silêncio.
const vistos = new Map([["index.html", "a capa (gerada)"]]);
for (const e of entradas) {
  if (vistos.has(e.arquivo)) falhar(`colisão: ${e.arquivo} <- ${vistos.get(e.arquivo)} + ${e.fonte}`);
  else vistos.set(e.arquivo, e.fonte);
}

const publicadas = entradas.filter((e) => e.publicada);
const paginaPorFonte = new Map(publicadas.map((e) => [e.fonte, e.arquivo]));
const emEscrita = new Set(entradas.filter((e) => !e.publicada).map((e) => e.fonte));

// ---------------------------------------------------------------------------
// Markdown
// ---------------------------------------------------------------------------
// Âncora no padrão do GitHub (mantém acento, tira pontuação, espaço -> hífen), para o
// mesmo "#secao" funcionar lendo no GitHub e no site.
const slugGitHub = (s) => s.trim().toLowerCase().replace(/[^\p{L}\p{M}\p{N}\s_-]/gu, "").replace(/\s/g, "-");
const md = new MarkdownIt({ html: true, linkify: false, typographer: false }).use(anchor, {
  slugify: slugGitHub,
  permalink: anchor.permalink.ariaHidden({ symbol: "#", placement: "after" }),
});

const imagens = new Map(); // destino em docs/ -> origem absoluta
const ancorasPendentes = []; // { origem, pagina, ancora }

// Link relativo: página publicada -> .html; arquivo/pasta do repositório que não é página
// (maestro-handbook/, claims.md, scripts do exemplo...) -> URL do GitHub; alvo que não
// existe -> FALHA. Link absoluto (http, mailto) passa intacto.
function resolverHref(href, env) {
  if (!href || /^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith("//")) return href;
  const i = href.indexOf("#");
  const semHash = i < 0 ? href : href.slice(0, i);
  const hash = i < 0 ? "" : href.slice(i + 1);
  if (!semHash) {
    if (hash) ancorasPendentes.push({ origem: env.fonte, pagina: env.arquivo, ancora: hash });
    return href;
  }
  const alvo = decod(semHash.split("?")[0]);
  let rel = alvo.startsWith("/") ? path.posix.normalize(alvo.slice(1)) : path.posix.normalize(path.posix.join(env.dir, alvo));
  rel = rel.replace(/\/+$/, "");
  if (rel === "." || rel === "") rel = "";
  if (rel.startsWith("..")) return reprovar(env, "link sai do repositório", href);
  // Capítulo declarado no sumário mas ainda em escrita: aponta para a capa, não falha.
  if (emEscrita.has(rel)) return "index.html";
  if (rel && !existeExato(rel)) return reprovar(env, "link quebrado (alvo não existe)", href);
  const anc = hash ? `#${hash}` : "";
  let pagina = paginaPorFonte.get(rel);
  if (!pagina && ehDir(rel)) pagina = paginaPorFonte.get(`${rel}/README.md`);
  if (pagina) {
    if (hash) ancorasPendentes.push({ origem: env.fonte, pagina, ancora: hash });
    return pagina + anc;
  }
  return (ehDir(rel) || !rel ? TREE : BLOB) + encodeURI(rel) + anc;
}

function resolverSrc(src, env) {
  if (!src || /^[a-z][a-z0-9+.-]*:/i.test(src) || src.startsWith("//")) return src;
  const rel = path.posix.normalize(path.posix.join(env.dir, decod(src.split("#")[0].split("?")[0])));
  if (rel.startsWith("..") || !existeExato(rel) || ehDir(rel)) return reprovar(env, "imagem quebrada", src);
  const destino = `img/${rel}`;
  imagens.set(destino, resolve(RAIZ, rel));
  return encodeURI(destino);
}

const padrao = (nome) => md.renderer.rules[nome] || ((t, i, o, e, s) => s.renderToken(t, i, o));
const linkOpen = padrao("link_open");
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href");
  if (href) tokens[idx].attrSet("href", resolverHref(href, env));
  return linkOpen(tokens, idx, options, env, self);
};
const image = padrao("image");
md.renderer.rules.image = (tokens, idx, options, env, self) => {
  tokens[idx].attrSet("src", resolverSrc(tokens[idx].attrGet("src"), env));
  return image(tokens, idx, options, env, self);
};
// HTML embutido no Markdown não passa pelas regras acima: reescreve href/src com a MESMA regra.
const reescreverHtml = (html, env) =>
  html
    .replace(/(<a\b[^>]*?\bhref=")([^"]*)(")/gi, (_, a, h, b) => a + resolverHref(h, env) + b)
    .replace(/(<img\b[^>]*?\bsrc=")([^"]*)(")/gi, (_, a, s, b) => a + resolverSrc(s, env) + b);
md.renderer.rules.html_block = (t, i, o, env) => reescreverHtml(t[i].content, env);
md.renderer.rules.html_inline = (t, i, o, env) => reescreverHtml(t[i].content, env);

// Seções da anatomia que ganham destaque visual (guia-editorial.md).
const CALLOUTS = [
  { re: /^pergunta central/i, cls: "c-obj", rot: "Pergunta" },
  { re: /^a falha real/i, cls: "c-falha", rot: "Caso real" },
  { re: /^exemplo execut/i, cls: "c-prat", rot: "Mão na massa" },
  { re: /^contraexemplo/i, cls: "c-contra", rot: "Limite" },
  { re: /^checklist/i, cls: "c-verif", rot: "Aplique" },
];
const marcarCallouts = (html) =>
  html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/g, (full, attrs, tit) => {
    const t = CALLOUTS.find((x) => x.re.test(tit.replace(/<[^>]+>/g, "").trim()));
    return t ? `<h2${attrs} class="callout ${t.cls}" data-rotulo="${t.rot}">${tit}</h2>` : full;
  });

// ---------------------------------------------------------------------------
// Molde
// ---------------------------------------------------------------------------
const grupos = [];
for (const e of entradas) {
  let g = grupos.find((x) => x.nome === e.grupo);
  if (!g) grupos.push((g = { nome: e.grupo, itens: [] }));
  g.itens.push(e);
}

const navLateral = (atual) =>
  grupos
    .map((g) =>
      `<div class="nav-parte">${esc(g.nome)}</div><ul>` +
      g.itens
        .map((e) => {
          const cls = [e.filho ? "filho" : "", e.arquivo === atual ? "ativo" : ""].filter(Boolean).join(" ");
          return e.publicada
            ? `<li${e.filho ? ' class="filho"' : ""}><a${cls ? ` class="${cls}"` : ""}${e.arquivo === atual ? ' aria-current="page"' : ""} href="${e.arquivo}">${esc(e.rotulo)}</a></li>`
            : `<li><span class="pendente" title="em escrita">${esc(e.rotulo)}</span></li>`;
        })
        .join("") +
      `</ul>`)
    .join("");

const btn = (e, dir) =>
  e ? `<a class="pg-${dir}" href="${e.arquivo}"><small>${dir === "prev" ? "← anterior" : "próximo →"}</small>${esc(e.titulo)}</a>` : `<span></span>`;

function pagina({ titulo, corpo, atual, prev, next, fonte, classe }) {
  return `<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(titulo)} · ${esc(S.titulo)}</title>
<meta name="description" content="${esc(S.subtitulo)}">
<script>try{var t=localStorage.getItem("tema");if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>
<link rel="stylesheet" href="assets/estilo.css">
</head><body${classe ? ` class="${classe}"` : ""}>
<header class="barra">
  <button id="alt-menu" aria-label="Abrir o sumário" aria-expanded="false" aria-controls="sidebar">☰ <span>Sumário</span></button>
  <a class="barra-titulo" href="index.html">${esc(S.titulo)}</a>
  <button id="alt-tema" aria-label="Alternar tema claro/escuro">◐</button>
</header>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <a class="marca" href="index.html">${esc(S.titulo)}<small>${esc(S.titulo_en || "")}</small></a>
    ${navLateral(atual)}
  </aside>
  <main class="conteudo">
    <article class="markdown">${corpo}</article>
    ${prev !== undefined ? `<nav class="paginacao" aria-label="Anterior e próximo">${btn(prev, "prev")}${btn(next, "next")}</nav>` : ""}
    <footer class="rodape">
      <a href="${REPO}">github.com/GHDaru/agentic_software_engineering</a>
      ${fonte ? ` · <a href="${BLOB}${encodeURI(fonte)}">fonte desta página</a>` : ""}
      · gerado de <code>livro/</code> por <code>publicar/build.mjs</code>
    </footer>
  </main>
</div>
<script src="assets/app.js"></script>
</body></html>`;
}

// ---------------------------------------------------------------------------
// Render (em memória; nada é escrito se houver falha)
// ---------------------------------------------------------------------------
const saidas = new Map(); // arquivo -> html
const idsPorPagina = new Map();
const CAPA = { arquivo: "index.html", titulo: "Capa" };

publicadas.forEach((e, k) => {
  const fonteMd = readFileSync(resolve(RAIZ, e.fonte), "utf8");
  const env = { fonte: e.fonte, arquivo: e.arquivo, dir: path.posix.dirname(e.fonte) };
  const corpo = marcarCallouts(md.render(fonteMd, env));
  idsPorPagina.set(e.arquivo, new Set([...corpo.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
  saidas.set(e.arquivo, pagina({ titulo: e.titulo, corpo, atual: e.arquivo, fonte: e.fonte,
    prev: k === 0 ? CAPA : publicadas[k - 1], next: publicadas[k + 1] || null }));
});

// Capa: título, subtítulo, as partes e o sumário completo.
const partesNome = (nome) => {
  const [rot, ...resto] = String(nome).split(" — ");
  return { rot, tit: resto.join(" — ") || rot };
};
const itemSumario = (e) =>
  e.publicada
    ? `<li${e.filho ? ' class="filho"' : ""}><a href="${e.arquivo}">${esc(e.rotulo)}</a></li>`
    : `<li class="pendente"><span>${esc(e.rotulo)}</span> <em>em escrita</em></li>`;
const capitulos = entradas.filter((e) => e.cap);
const escritos = capitulos.filter((e) => e.publicada).length;
const primeira = publicadas[0];
const corpoCapa =
  `<header class="capa">
    ${S.titulo_en ? `<p class="capa-sup">${esc(S.titulo_en)}</p>` : ""}
    <h1>${esc(S.titulo)}</h1>
    <p class="capa-sub">${esc(S.subtitulo)}</p>
    ${S.leitor ? `<p class="capa-leitor">Para quem: <strong>${esc(S.leitor)}</strong> · ${escritos} de ${capitulos.length} capítulos publicados</p>` : ""}
    ${primeira ? `<a class="capa-cta" href="${primeira.arquivo}">Começar a ler →</a>` : ""}
  </header>
  <h2 id="partes">As partes</h2>
  <div class="capa-partes">${(S.partes || [])
    .map((p) => {
      const { rot, tit } = partesNome(p.nome);
      const ns = (p.capitulos || []).map((c) => c.n);
      return `<div class="capa-parte"><span class="cp-rot">${esc(rot)}</span><span class="cp-tit">${esc(tit)}</span><span class="cp-caps">capítulos ${Math.min(...ns)}–${Math.max(...ns)}</span></div>`;
    })
    .join("")}</div>
  <h2 id="sumario">Sumário</h2>
  <div class="capa-sumario">${grupos
    .map((g) => `<div class="s-grupo"><div class="s-parte">${esc(g.nome)}</div><ul>${g.itens.map(itemSumario).join("")}</ul></div>`)
    .join("")}</div>`;
saidas.set("index.html", pagina({ titulo: "Capa", corpo: corpoCapa, atual: "index.html", classe: "p-capa", prev: null, next: primeira || null }));

// Âncoras: "#secao" para uma página publicada tem de existir nela.
for (const a of ancorasPendentes) {
  const ids = idsPorPagina.get(a.pagina);
  if (ids && !ids.has(a.ancora) && !ids.has(decod(a.ancora)))
    falhar(`${a.origem}: âncora inexistente -> ${a.pagina}#${decod(a.ancora)}`);
}

// Rede de segurança: todo href relativo do HTML final aponta para página ou arquivo gerado.
const ativos = new Set(["assets/estilo.css", "assets/app.js", ...imagens.keys()].map((x) => encodeURI(x)));
for (const [arq, html] of saidas) {
  for (const m of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const u = m[1];
    if (/^[a-z][a-z0-9+.-]*:/i.test(u) || u.startsWith("#") || u.startsWith("//")) continue;
    const alvo = u.split("#")[0];
    if (jaReprovados.has(`${arq}|${u}`)) continue;
    if (/\.md$/i.test(alvo)) falhar(`${arq}: link .md não reescrito -> ${u}`);
    else if (!saidas.has(alvo) && !ativos.has(alvo)) falhar(`${arq}: alvo não gerado -> ${u}`);
  }
}

if (falhas.length) {
  console.error(`✗ build reprovado: ${falhas.length} problema(s) — docs/ NÃO foi alterado.`);
  falhas.forEach((f) => console.error("   " + f));
  console.error("   → corrija o link/arquivo, ou publique o alvo (livro/sumario.yaml).");
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Escrita: limpa só o que o motor gera (preserva p.ex. um CNAME em docs/)
// ---------------------------------------------------------------------------
mkdirSync(SAIDA, { recursive: true });
for (const f of readdirSync(SAIDA)) if (f.endsWith(".html")) rmSync(resolve(SAIDA, f));
for (const d of ["assets", "img"]) rmSync(resolve(SAIDA, d), { recursive: true, force: true });
mkdirSync(resolve(SAIDA, "assets"), { recursive: true });
cpSync(resolve(AQUI, "tema/estilo.css"), resolve(SAIDA, "assets/estilo.css"));
cpSync(resolve(AQUI, "tema/app.js"), resolve(SAIDA, "assets/app.js"));
writeFileSync(resolve(SAIDA, ".nojekyll"), "");
for (const [destino, origem] of imagens) {
  mkdirSync(dirname(resolve(SAIDA, destino)), { recursive: true });
  cpSync(origem, resolve(SAIDA, destino));
}
for (const [arq, html] of saidas) writeFileSync(resolve(SAIDA, arq), html);

const pendentes = entradas.filter((e) => !e.publicada).map((e) => e.rotulo);
console.log(`✓ docs/ gerado: capa + ${publicadas.length} página(s), ${imagens.size} imagem(ns); links internos OK.`);
if (pendentes.length) console.log(`  em escrita (sem página, listados na capa): ${pendentes.length}`);
