# Blog-Django

## Visão Geral

**Blog-Django** é uma aplicação simples construída com Django, integrando frontend e backend no mesmo repositório. Permite criar, listar e visualizar posts de blog, além de incluir um sistema de autenticação de utilizadores (registo, login, logout).

Ideal para aprender os fundamentos de desenvolvimento web fullstack com Django.

---

## Funcionalidades Principais

- Criação, edição e visualização de posts de blog  
- Autenticação de utilizadores (registo, login, logout)  
- Rotas organizadas por aplicação (`blog` e `users`)  
- Upload e exibição de imagens nos posts  

---

## Estrutura do Projeto

```
blog-django/
├── blog_django/         # Configurações globais do Django (settings, URLs, WSGI)
├── blog/                # App principal do blog
│   ├── migrations/      # Arquivos de migração
│   ├── models.py        # Modelo Post
│   ├── views.py         # Views de listagem e detalhe
│   ├── urls.py          # Rotas da app blog
│   └── templates/blog/  # Templates HTML para listagem e detalhe
├── users/               # App para autenticação de utilizadores
│   ├── templates/users/ # Templates para registo, login e logout
│   └── urls.py          # Rotas de autenticação
├── media/               # Uploads de imagens dos posts
├── manage.py            # Script de gestão do Django
├── requirements.txt     # Lista de dependências
└── README.md            # Documentação do projeto
```

---

## Instalação

1. Clonar o repositório

```bash
git clone https://github.com/emanuelsoares97/blog-django.git
cd blog-django
```

2. Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar as dependências

```bash
pip install -r requirements.txt
```

4. Aplicar as migrações (SQLite por padrão)

```bash
python manage.py migrate
```

5. Criar superutilizador (opcional para admin)

```bash
python manage.py createsuperuser
```

6. Executar o servidor

```bash
python manage.py runserver
```

---

## Uso

- Aceda a: http://127.0.0.1:8000/  
- Registe-se ou inicie sessão para criar novos posts  
- A página principal lista todos os posts disponíveis  
- Clique num post para visualizar título, conteúdo e imagem  
- Área de administração: http://127.0.0.1:8000/admin/

---

## Tecnologias Utilizadas

- Python 3.x  
- Django 4.x  
- SQLite (enquanto não for feito o deploy)  
- HTML/CSS (bootstrap)

---

## Possíveis Melhorias Futuras

- Sistema de comentários para os posts 
- Sistema de likes para os posts  
- Deploy em ambiente de produção (Render, Railway, etc.)  
- Testes automatizados (pytest ou Django TestCase)


---

## Licença

Este projeto é de uso educativo e livre para fins não comerciais. Sinta-se à vontade para usar como base para projetos próprios.
