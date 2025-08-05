"""
Base de Conhecimento do InventarioPro
Contém informações sobre o sistema para responder perguntas dos usuários
"""

KNOWLEDGE_BASE = {
    "sistema_geral": {
        "descricao": "InventarioPro é um sistema de gestão de inventário para eventos",
        "funcionalidades": [
            "Gestão de eventos com datas e locais",
            "Controle de produtos e categorias",
            "Gestão de estoque geral e por sala",
            "Sistema de propostas comerciais",
            "Dashboard com estatísticas",
            "Assistente de IA integrado"
        ]
    },
    
    "eventos": {
        "como_criar": "Acesse 'Eventos' no menu lateral e clique em 'Novo Evento'. Preencha nome, descrição, datas e local. Use o assistente de IA para melhorar a descrição.",
        "campos_obrigatorios": ["nome", "data_inicial"],
        "campos_opcionais": ["descricao", "data_final", "local", "imagem"],
        "dicas": [
            "Use o assistente de IA para gerar descrições profissionais",
            "Adicione imagens para tornar eventos mais atrativos",
            "Configure salas específicas para cada evento",
            "Defina datas de início e fim para melhor controle"
        ]
    },
    
    "produtos": {
        "como_criar": "Vá em 'Produtos' e clique em 'Novo Produto'. Defina nome, categoria, preço e descrição.",
        "campos_obrigatorios": ["nome", "preco"],
        "campos_opcionais": ["categoria", "descricao", "imagem"],
        "precos": "Preços devem ser em reais (BRL) com formato decimal (ex: 99.90)",
        "categorias": "Use categorias para organizar produtos similares",
        "dicas": [
            "Use o assistente de IA para sugerir produtos baseados em descrições",
            "Organize produtos em categorias para facilitar busca",
            "Mantenha preços atualizados",
            "Adicione descrições detalhadas"
        ]
    },
    
    "estoque": {
        "tipos": {
            "geral": "Estoque total de cada produto no sistema",
            "por_sala": "Estoque específico de produtos em salas de eventos"
        },
        "como_gerenciar": "Acesse 'Estoque Geral' para controle global ou vá em eventos específicos para gerenciar estoque por sala",
        "alertas": "O sistema alerta quando produtos têm menos de 10 unidades",
        "dicas": [
            "Monitore regularmente produtos com baixo estoque",
            "Use estoque por sala para eventos específicos",
            "Mantenha registros atualizados de entrada e saída",
            "Configure alertas para reposição"
        ]
    },
    
    "propostas": {
        "como_criar": "Vá em 'Propostas' e clique em 'Nova Proposta'. Selecione evento e adicione produtos com quantidades",
        "campos_obrigatorios": ["evento"],
        "calculo_valor": "Valor total é calculado automaticamente baseado nos produtos e quantidades",
        "dicas": [
            "Vincule propostas aos eventos correspondentes",
            "Revise valores antes de finalizar",
            "Use para orçamentos e controle financeiro",
            "Gere relatórios para análise de vendas"
        ]
    },
    
    "dashboard": {
        "funcionalidades": [
            "Estatísticas gerais do sistema",
            "Contadores de eventos, produtos, salas e propostas",
            "Lista de eventos e propostas recentes",
            "Alertas de produtos com baixo estoque",
            "Ações rápidas para criar novos itens",
            "Valor total das propostas"
        ],
        "como_usar": "O dashboard é a página inicial após login. Mostra visão geral e permite acesso rápido às funcionalidades",
        "dicas": [
            "Use como ponto de partida para navegação",
            "Monitore alertas de estoque",
            "Acesse ações rápidas para criar itens",
            "Acompanhe estatísticas regularmente"
        ]
    },
    
    "navegacao": {
        "menu_lateral": "Use o menu lateral para acessar todas as funcionalidades",
        "breadcrumbs": "Acompanhe sua localização através dos breadcrumbs",
        "busca": "Use campos de busca para encontrar itens específicos",
        "filtros": "Aplique filtros para refinar resultados"
    },
    
    "assistente_ia": {
        "funcionalidades": [
            "Melhoria automática de descrições de eventos",
            "Sugestões de produtos baseadas em descrições",
            "Chat para perguntas sobre o sistema",
            "Geração de relatórios e resumos",
            "Ajuda contextual em cada página"
        ],
        "como_usar": {
            "eventos": "Use o botão 'Melhorar com IA' nos formulários de eventos",
            "produtos": "Digite uma descrição no assistente de produtos para receber sugestões",
            "chat": "Clique no ícone de chat no canto inferior direito",
            "ajuda": "Pergunte qualquer coisa sobre o sistema no chat"
        }
    },
    
    "solucao_problemas": {
        "login": {
            "problema": "Não consegue fazer login",
            "solucoes": [
                "Verifique usuário e senha",
                "Certifique-se de que a conta está ativa",
                "Limpe cache do navegador",
                "Entre em contato com administrador"
            ]
        },
        "performance": {
            "problema": "Sistema lento",
            "solucoes": [
                "Verifique conexão com internet",
                "Feche outras abas do navegador",
                "Limpe cache e cookies",
                "Use navegador atualizado"
            ]
        },
        "dados": {
            "problema": "Dados não aparecem",
            "solucoes": [
                "Recarregue a página",
                "Verifique filtros aplicados",
                "Certifique-se de ter permissões",
                "Verifique se dados foram salvos corretamente"
            ]
        }
    },
    
    "boas_praticas": {
        "organizacao": [
            "Use categorias consistentes para produtos",
            "Mantenha nomes descritivos e padronizados",
            "Organize eventos por datas e tipos",
            "Faça backup regular dos dados"
        ],
        "seguranca": [
            "Use senhas fortes",
            "Faça logout ao sair",
            "Não compartilhe credenciais",
            "Mantenha dados atualizados"
        ],
        "eficiencia": [
            "Use atalhos e ações rápidas",
            "Configure alertas de estoque",
            "Revise dados regularmente",
            "Use o assistente de IA para automatizar tarefas"
        ]
    }
}

def get_knowledge_for_topic(topic):
    """Retorna conhecimento específico sobre um tópico"""
    return KNOWLEDGE_BASE.get(topic, {})

def search_knowledge(query):
    """Busca conhecimento baseado em uma consulta"""
    query_lower = query.lower()
    results = []
    
    for topic, content in KNOWLEDGE_BASE.items():
        if query_lower in topic.lower():
            results.append((topic, content))
            continue
            
        if isinstance(content, dict):
            for key, value in content.items():
                if query_lower in key.lower():
                    results.append((f"{topic}.{key}", value))
                elif isinstance(value, str) and query_lower in value.lower():
                    results.append((f"{topic}.{key}", value))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str) and query_lower in item.lower():
                            results.append((f"{topic}.{key}", item))
    
    return results

def get_contextual_help(page_context):
    """Retorna ajuda contextual baseada na página atual"""
    context_map = {
        'dashboard': 'dashboard',
        'eventos': 'eventos',
        'produtos': 'produtos',
        'estoque': 'estoque',
        'propostas': 'propostas'
    }
    
    for key, topic in context_map.items():
        if key in page_context.lower():
            return get_knowledge_for_topic(topic)
    
    return get_knowledge_for_topic('sistema_geral')

# Perguntas frequentes pré-definidas
FAQ_COMUM = [
    {
        "pergunta": "Como criar um novo evento?",
        "resposta": "Acesse 'Eventos' no menu lateral, clique em 'Novo Evento', preencha os campos obrigatórios (nome e data inicial) e use o assistente de IA para melhorar a descrição."
    },
    {
        "pergunta": "Como controlar o estoque?",
        "resposta": "Use 'Estoque Geral' para controle global ou acesse eventos específicos para gerenciar estoque por sala. O sistema alerta quando produtos têm menos de 10 unidades."
    },
    {
        "pergunta": "Como funciona o assistente de IA?",
        "resposta": "O assistente pode melhorar descrições de eventos, sugerir produtos, responder perguntas sobre o sistema e gerar relatórios. Use o botão 'Melhorar com IA' nos formulários ou o chat no canto da tela."
    },
    {
        "pergunta": "Como criar uma proposta?",
        "resposta": "Vá em 'Propostas', clique em 'Nova Proposta', selecione um evento e adicione produtos com quantidades. O valor total é calculado automaticamente."
    },
    {
        "pergunta": "Como organizar produtos?",
        "resposta": "Use categorias para agrupar produtos similares, mantenha nomes descritivos e preços atualizados em reais (BRL)."
    }
]

