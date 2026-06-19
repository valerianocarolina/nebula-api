# Nebula API

API REST desenvolvida com Django REST Framework para a rede social Nebula.

## Funcionalidades

### Autenticação

* Cadastro de usuários
* Login com JWT
* Refresh Token
* Logout

### Usuários

* Perfil público e privado
* Atualização de perfil
* Alteração de senha
* Busca de usuários

### Posts

* Criação de posts
* Upload de imagens e vídeos
* Hashtags
* Feed personalizado
* Pesquisa de posts

### Interações

* Curtidas
* Comentários
* Amizades
* Seguir usuários

### Mensagens

* Conversas privadas
* Envio de mensagens
* Controle de leitura

### Moderação

* Sistema de denúncias
* Painel administrativo
* Dashboard de métricas

## Tecnologias

* Python 3.12
* Django 6
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Docker
* Gunicorn
* WhiteNoise
* Pytest

## Instalação Local

### Clonar o projeto

```bash
git clone <url-do-repositorio>
cd nebula-api
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Configurar variáveis de ambiente

Criar arquivo:

```text
.env
```

Baseado em:

```text
.env.example
```

### Executar migrações

```bash
python manage.py migrate
```

### Criar superusuário

```bash
python manage.py createsuperuser
```

### Executar servidor

```bash
python manage.py runserver
```

## Docker

Subir ambiente completo:

```bash
docker compose up --build
```

## Documentação

Swagger:

```text
http://localhost:8000/api/docs/
```

Schema OpenAPI:

```text
http://localhost:8000/api/schema/
```

## Testes

```bash
pytest
```

## Licença

Projeto desenvolvido para fins educacionais e de aprendizado.
