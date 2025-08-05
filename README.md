# InventarioPro v2 - Sistema de Gestão de Inventário

Um sistema completo de gestão de inventário para eventos, desenvolvido em Django com interface moderna e responsiva.

## 🚀 Características

- **Dashboard Interativo**: Visão geral com estatísticas em tempo real
- **Gestão de Eventos**: Criação e gerenciamento de eventos
- **Controle de Estoque**: Gestão de produtos e quantidades
- **Sistema de Propostas**: Criação e acompanhamento de propostas
- **Interface Moderna**: Design responsivo e profissional
- **Autenticação Segura**: Sistema de login integrado

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone ou extraia o projeto**
   ```bash
   cd inventariopro_v2
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute as migrações do banco de dados**
   ```bash
   python manage.py migrate
   ```

4. **Crie um superusuário (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Colete os arquivos estáticos**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Inicie o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

7. **Acesse o sistema**
   - Abra seu navegador e vá para: `http://localhost:8000`
   - Faça login com as credenciais criadas

## 👤 Usuário de Teste

Para facilitar os testes, você pode criar um usuário administrador:

- **Usuário**: admin
- **Senha**: admin123

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
>>> exit()
```

## 📱 Funcionalidades

### Dashboard
- Estatísticas gerais do sistema
- Contadores de eventos, produtos, salas e propostas
- Alertas de baixo estoque
- Ações rápidas para criação de itens

### Gestão de Eventos
- Criação e edição de eventos
- Upload de imagens
- Definição de datas e locais
- Gerenciamento de salas por evento

### Controle de Produtos
- Cadastro de produtos com preços
- Categorização de produtos
- Controle de estoque geral
- Estoque por sala/evento

### Sistema de Propostas
- Criação de propostas para eventos
- Cálculo de valores totais
- Histórico de propostas
- Detalhamento completo

## 🎨 Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Ícones**: BoxIcons
- **Fontes**: Google Fonts (Inter)
- **Banco de Dados**: SQLite (padrão)
- **Moeda**: django-money para valores monetários

## 📁 Estrutura do Projeto

```
inventariopro_v2/
├── camarim/                    # App principal
│   ├── static/camarim/        # Arquivos estáticos
│   │   ├── css/               # Estilos customizados
│   │   └── js/                # JavaScript
│   ├── templates/             # Templates HTML
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views/Controllers
│   └── urls.py                # URLs do app
├── project/                   # Configurações do projeto
├── media/                     # Uploads de arquivos
├── staticfiles/               # Arquivos estáticos coletados
├── manage.py                  # Script de gerenciamento Django
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🔒 Configurações de Segurança

Para uso em produção, certifique-se de:

1. Alterar a `SECRET_KEY` no arquivo `settings.py`
2. Definir `DEBUG = False`
3. Configurar `ALLOWED_HOSTS` adequadamente
4. Usar um banco de dados robusto (PostgreSQL, MySQL)
5. Configurar HTTPS
6. Implementar backup regular dos dados

## 🆘 Suporte

Para dúvidas ou problemas:

1. Verifique se todas as dependências estão instaladas
2. Certifique-se de que as migrações foram executadas
3. Verifique os logs do Django para erros específicos

## 📄 Licença

Este projeto é de uso interno e educacional.

## 🎯 Próximos Passos

- Implementar relatórios em PDF
- Adicionar gráficos interativos
- Sistema de notificações
- API REST para integração
- Backup automático de dados

---

**InventarioPro v2** - Sistema de Gestão de Inventário Profissional

