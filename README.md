# Blog-Django

## Visão Geral

Blog-Django é uma aplicação de blog completa construída com Django (frontend + backend no mesmo repositório). Permite criar, editar e visualizar posts, com autenticação (registo, login, logout) e recursos adicionais como comentários, likes, perfis com avatar e destaques. O projeto evoluiu a partir de um tutorial do Corey Schafer e foi expandido com novas funcionalidades, melhorias de UX e pipeline de deploy.

Ideal para aprender desenvolvimento web fullstack com Django, integrando autenticação, templates, gestão de ficheiros estáticos e deploy containerizado.

---

## Funcionalidades Principais

- Autenticação de utilizadores (registo, login, logout) e social login (Google)
- CRUD de posts, comentários e likes
- Perfis de utilizador com avatar (armazenamento em cloud)
- Página inicial com feed e destaques (mais likes/comentários)
- Notificações e mensagens privadas entre utilizadores
- Admin para gestão rápida de conteúdo
- UI responsiva com templates reutilizáveis

---

## Arquitetura e Tecnologias

- Backend: Python, Django 5, Django Allauth
- Base de Dados: PostgreSQL
- Ficheiros estáticos: WhiteNoise (Compressed Manifest)
- Media (uploads): Cloudinary
- Infra: Docker (imagem e runtime)
- CI/CD: GitHub Actions (testes, build, deploy)
- Frontend: HTML, CSS, JavaScript (templates Django)

---

## Estrutura do Projeto (simplificada)

blog-django/
├── blog_django/               # Settings, URLs, WSGI
├── blog/                      # App principal (posts, likes, comentários)
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── static/blog/           # main.css, likes.js, comments.js, assets da app
│   └── templates/blog/        # Templates HTML
├── users/                     # App de utilizadores/autenticação
│   ├── adapters.py            # Integração social (ex.: Google)
│   ├── forms.py, models.py
│   ├── urls.py
│   └── templates/users/
├── notifications/             # Notificações (app dedicada)
├── private_messages/          # Mensagens privadas (app dedicada)
├── staticfiles/               # Saída do collectstatic (gerada em build/deploy)
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml (se aplicável)
└── README.md

---

## Pré-requisitos

- Python 3.10+
- PostgreSQL 13+ (ou usa SQLite localmente para desenvolvimento)
- Conta Cloudinary (para armazenar avatares/media) — opcional em dev
- Docker (opcional, mas recomendado para produção)

---

## Instalação (Local)

1) Clonar o repositório
- git clone https://github.com/emanuelsoares97/blog-django.git
- cd blog-django

2) Criar e ativar ambiente virtual
- python -m venv venv
- No Windows: venv\Scripts\activate
- No Linux/Mac: source venv/bin/activate

3) Instalar dependências
- pip install -r requirements.txt

4) Variáveis de ambiente (ficheiro .env em desenvolvimento)
- SECRET_KEY=uma_chave_segura
- DB_NAME=blog
- DB_USER=postgres
- DB_PASSWORD=postgres
- DB_HOST=127.0.0.1
- DB_PORT=5432
- DJANGO_ENV=development
- (Opcional para Cloudinary)
  - CLOUDINARY_CLOUD_NAME=...
  - CLOUDINARY_API_KEY=...
  - CLOUDINARY_API_SECRET=...

5) Migrar a base de dados
- python manage.py migrate

6) Criar superutilizador (opcional)
- python manage.py createsuperuser

7) Executar o servidor
- python manage.py runserver
- Aceder a http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Gestão de Ficheiros Estáticos e Media

- Estáticos da app: colocar em app/static/app/ (ex.: blog/static/blog/main.css)
- Collectstatic (gera para STATIC_ROOT):
  - python manage.py collectstatic
- Em produção, os estáticos são servidos via WhiteNoise.
- Media (uploads de avatar/perfil) são armazenados na cloud (Cloudinary). Em desenvolvimento, pode-se usar localmente se preferires (ajusta DEFAULT_FILE_STORAGE e MEDIA_*).

---

## Testes

- Executar todos os testes:
  - python manage.py test
- A pipeline de CI (GitHub Actions) executa testes em cada push/PR.

---

## Docker (Opcional)

- Build local da imagem:
  - docker build . -t blog-app:local
- Executar com docker-compose (se configurado):
  - docker compose up --build

---

## Deploy (CI/CD)

- Pipeline CI/CD no GitHub Actions:
  - Build da imagem Docker
  - Execução de testes
  - Deploy automático em produção (container)
  - Collectstatic executado durante o build/deploy

Configura as secrets necessárias no repositório (SECRET_KEY, DB_*, credenciais de Cloudinary, etc.).

---

## Roadmap (Próximos Passos)

- Acessibilidade (a11y) e SEO (headings semânticos, alt text, meta tags)
- Mais testes de integração e cobertura
- Otimizações de performance e caching
- Monitorização e alertas de erros em produção

---

## Créditos e Inspiração

Este projeto foi inicialmente inspirado e desenvolvido com base num tutorial do Corey Schafer, mas desde então foi expandido com novas funcionalidades como comentários, likes e autenticação social para proporcionar uma experiência mais rica.

---

## Licença

Uso educativo e livre para fins não comerciais. Sinta-se à vontade para adaptar e evoluir este projeto.
