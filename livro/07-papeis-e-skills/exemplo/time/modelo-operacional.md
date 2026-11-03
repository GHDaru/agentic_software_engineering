# Modelo operacional do time (fixture do capítulo 7)

Cada papel é um modo de trabalho. Os humanos não têm arquivo de perfil: decidem e respondem.
Os papéis de agente abaixo são a **norma**; o `confere.py` exige que cada um tenha um
perfil executável em `papeis/`, e que cada perfil em `papeis/` seja um papel desta tabela.

| Papel | Exercido por | Responsabilidade | Gate |
|---|---|---|---|
| **Responsável pelo produto** | Humano | Decide o quê e o porquê; aprova spec e merge | Accountable de tudo |
| **Especificador** | Agente | Escreve a spec a partir da intenção; levanta ambiguidades | Humano aprova a spec |
| **Arquiteto** | Agente | Escreve o plano e o confere contra os princípios | Humano aprova o plano |
| **Semântica de interface** | Agente | Declara o papel de cada objeto de tela antes do componente | Papel antes do componente |
| **Implementador** | Agente | Implementa uma tarefa por vez, com testes | Testes verdes |
| **Revisor** | Agente em contexto fresco | Revisa o diff contra o plano; aponta lacunas, não corrige | Gate de merge |
| **Segurança** | Agente | Injeção, segredos e autorização no diff | Gate de segurança |
