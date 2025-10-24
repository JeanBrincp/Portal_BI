# PORTAL BI

Projeto Django para portal de dashboards.

Visão rápida
- Django 5.x
- Banco padrão: SQLite (padrão em `settings.py`) — recomendado usar PostgreSQL em produção
- Start: `gunicorn portal.wsgi:application`

Arquivos importantes adicionados
- `.gitignore` — exclui venv, db.sqlite3, media e arquivos locais
- `Procfile` — para deploy em PaaS (ex.: Railway, Heroku)

Como subir para um repositório Git (passo-a-passo)
1. No seu computador, entre na pasta do projeto:
   ```powershell
   cd "C:\Users\jean.costa\Desktop\02 - PORTAL BI\portal_bi"
   ```
2. Inicializar repositório e fazer commit (já foi feito localmente por este script):
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: preparar projeto para repo"
   ```
3. Criar um repositório remoto (GitHub/GitLab/Bitbucket) via interface web.
4. Adicionar o remote e enviar (substitua `<remote-url>`):
   ```powershell
   git remote add origin <remote-url>
   git branch -M main
   git push -u origin main
   ```

Deploy no Railway (resumo)
1. Criar novo Project -> Deploy from GitHub -> selecione o repositório.
2. Defina variáveis de ambiente: `SECRET_KEY`, `DEBUG=false`, `ALLOWED_HOSTS`.
3. Se quiser persistência, adicione o plugin PostgreSQL e deixe o Railway preencher `DATABASE_URL`.
4. Em Start Command coloque: `gunicorn portal.wsgi:application --bind 0.0.0.0:$PORT`

Observações
- O `db.sqlite3` está no `.gitignore` por boa prática. Se quiser versionar o banco (não recomendado), remova do `.gitignore`.
- Garanta `SECRET_KEY` e outras variáveis por environment variables antes de expor o app.
