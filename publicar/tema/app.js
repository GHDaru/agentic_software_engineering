// Tema claro/escuro (lembrado no navegador) e sumário recolhível no celular. Sem dependências.
(function () {
  var r = document.documentElement;
  var tema = document.getElementById("alt-tema");
  if (tema) tema.addEventListener("click", function () {
    var escuro = r.getAttribute("data-theme") === "dark" ||
      (!r.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var novo = escuro ? "light" : "dark";
    r.setAttribute("data-theme", novo);
    try { localStorage.setItem("tema", novo); } catch (e) {}
  });

  var menu = document.getElementById("alt-menu");
  var lateral = document.getElementById("sidebar");
  if (menu && lateral) {
    menu.addEventListener("click", function () {
      var aberto = document.body.classList.toggle("menu-aberto");
      menu.setAttribute("aria-expanded", aberto ? "true" : "false");
    });
    lateral.addEventListener("click", function (ev) {
      if (ev.target.closest("a")) document.body.classList.remove("menu-aberto");
    });
  }
  // Mantém o item ativo visível na lateral.
  var ativo = document.querySelector(".sidebar a.ativo");
  if (ativo && lateral && lateral.scrollHeight > lateral.clientHeight)
    lateral.scrollTop = Math.max(0, ativo.offsetTop - lateral.clientHeight / 2);
})();
