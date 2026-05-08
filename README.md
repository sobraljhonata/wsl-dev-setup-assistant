# WSL Dev Setup Assistant

Aplicação desktop educacional construída com Kivy para facilitar o onboarding de usuários Windows no WSL, Linux e terminal.

---

## 🎯 Objetivo

O projeto busca reduzir a barreira inicial de uso do Linux para estudantes e iniciantes em desenvolvimento, guiando:

* instalação do WSL
* escolha de distribuições Linux
* criação do primeiro usuário Linux
* aprendizado básico de terminal
* uso assistido do Dev Setup CLI

O objetivo não é esconder o Linux, mas ajudar o usuário a aprender Linux com segurança e contexto.

---

## 👨‍🏫 Público-alvo

* estudantes iniciantes em programação
* alunos aprendendo Linux e terminal
* usuários Windows sem experiência com WSL
* onboarding técnico em ambientes educacionais

---

## ✨ Funcionalidades atuais

* Verificação do WSL
* Listagem de distribuições disponíveis
* Instalação de distro Linux
* Primeira execução da distro
* Orientação para criação de usuário Linux
* Terminal assistido
* Instalação do Dev Setup CLI
* Execução guiada de:

  * `devsetup --help`
  * `devsetup doctor`
  * `devsetup --dry-run`

---

## 🏗️ Arquitetura

```text
UI (Kivy Screens)
        ↓
Services Layer
        ↓
WSL Integration
        ↓
subprocess / wsl.exe
```

---

## ⚙️ Requisitos

* Windows 10/11
* WSL habilitado
* Python 3.12 link para download [Microsoft](https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=pt-BR&gl=BR) ou [Repo Python Oficial](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe)
* pip
* Git

---

## 📦 Instalação

### Criar ambiente virtual

```powershell
py -3.12 -m venv .venv
```

### Ativar ambiente virtual

```powershell
.\.venv\Scripts\activate
```

### Atualizar ferramentas básicas

```powershell
python -m pip install --upgrade pip setuptools wheel
```

### Instalar dependências

```powershell
pip install -e ".[dev]"
```

---

## ▶️ Executar aplicação

```powershell
python -m app.main
```

---

## 🧠 Fluxo educacional

O fluxo atual da aplicação é:

```text
Welcome
→ Verificar WSL
→ Escolher distro
→ Instalar distro
→ Primeira execução Linux
→ Terminal assistido
```

---

## 🖥️ Screenshots

> Adicionar screenshots e GIFs do fluxo da aplicação.

---

## ⚠️ Limitações atuais

* Algumas instalações podem solicitar senha Linux (`sudo`)
* Primeira execução da distro ainda depende do terminal do WSL
* O projeto está em fase de PoC/MVP

---

## 🛣️ Roadmap

* [ ] Melhorias visuais com múltiplas telas
* [ ] Histórico de comandos
* [ ] Terminal mais interativo
* [ ] Build `.exe` com PyInstaller
* [ ] Modo aula com cards educacionais
* [ ] Testes automatizados
* [ ] Download automático de dependências
* [ ] Suporte a múltiplos profiles Dev Setup

---

## 🤝 Contribuição

Pull requests são bem-vindos.

---

## 📄 Licença

MIT

---

## 💡 Relacionado

Este projeto funciona em conjunto com:

* Dev Setup CLI
* WSL
* Windows Terminal
