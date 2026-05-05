# Dev Setup Launcher

Aplicação desktop educacional em Kivy para facilitar o onboarding de alunos no WSL, Linux e Dev Setup CLI.

## Objetivo

Reduzir a barreira inicial de uso do Linux/terminal para usuários Windows, guiando a instalação do WSL, a escolha de uma distro Linux e o uso assistido do Dev Setup CLI.

## MVP

- Verificar WSL
- Listar distros disponíveis
- Instalar distro
- Abrir primeira execução da distro
- Orientar criação de usuário Linux
- Terminal assistido
- Instalar e executar Dev Setup CLI
- Explicar comandos como `doctor`, `--help` e `--dry-run`

## Rodar

```bash
pip install -e ".[dev]"
python -m app.main

sudo apt update
sudo apt install -y libmtdev1 xclip xsel
```