import os
import re
import logging
import openai
from django.conf import settings

logger = logging.getLogger(__name__)
api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error('OPENAI_API_KEY não encontrado. Defina em settings ou como env var.')
else:
    openai.api_key = api_key

def send_chat(prompt: str, model: str='gpt-4o-mini',
              system_message: str=None, temperature: float=0.7,
              max_tokens: int=512) -> str:
    """
    Envia uma mensagem para o modelo de IA e retorna a resposta.
    
    Args:
        prompt: Mensagem do usuário
        model: Modelo a ser usado (padrão: gpt-4o-mini)
        system_message: Mensagem de sistema para contexto
        temperature: Criatividade da resposta (0-1)
        max_tokens: Máximo de tokens na resposta
        
    Returns:
        Resposta do modelo de IA
    """
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = openai.ChatCompletion.create(
            model=model, 
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens
        )
        return resp.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        logger.error(f"Erro OpenAI API: {e}", exc_info=True)
        return "Desculpe, não consegui processar sua requisição agora. Tente mais tarde."

# Funções específicas para o InventarioPro

def generate_event_description(draft_text: str) -> dict:
    """
    Gera uma descrição polida para um evento baseada em um rascunho.
    
    Args:
        draft_text: Rascunho do usuário
        
    Returns:
        Dict com título, descrição e instruções sugeridas
    """
    system_message = """
    Você é um assistente especializado em eventos e inventário. 
    Sua tarefa é transformar rascunhos de eventos em descrições profissionais e organizadas.
    Retorne sempre um JSON com as chaves: titulo, descricao, local_sugerido, instrucoes_acesso.
    Seja conciso mas informativo.
    """
    
    prompt = f"""
    Transforme este rascunho em uma descrição profissional de evento:
    
    "{draft_text}"
    
    Gere um JSON com:
    - titulo: Título atrativo e profissional
    - descricao: Descrição detalhada e bem estruturada
    - local_sugerido: Sugestão de local se não especificado
    - instrucoes_acesso: Instruções básicas de acesso/participação
    """
    
    response = send_chat(prompt, system_message=system_message, temperature=0.3)
    
    try:
        import json
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "titulo": "Evento",
            "descricao": response,
            "local_sugerido": "",
            "instrucoes_acesso": ""
        }

def suggest_products_categories(description: str) -> dict:
    """
    Sugere produtos e categorias baseado em uma descrição.
    
    Args:
        description: Descrição do que é necessário
        
    Returns:
        Dict com produtos e categorias sugeridas
    """
    system_message = """
    Você é um especialista em inventário e gestão de produtos.
    Analise a descrição fornecida e sugira produtos específicos e categorias relevantes.
    Retorne um JSON com: produtos (lista de objetos com nome, categoria, preco_estimado) e categorias (lista de strings).
    """
    
    prompt = f"""
    Baseado nesta necessidade, sugira produtos e categorias:
    
    "{description}"
    
    Retorne um JSON com:
    - produtos: [{"nome": "...", "categoria": "...", "preco_estimado": "R$ XX,XX"}]
    - categorias: ["categoria1", "categoria2", ...]
    """
    
    response = send_chat(prompt, system_message=system_message, temperature=0.4)
    
    try:
        import json
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "produtos": [],
            "categorias": []
        }

def answer_faq(question: str, context: str = None) -> str:
    """
    Responde perguntas sobre o sistema InventarioPro.
    
    Args:
        question: Pergunta do usuário
        context: Contexto adicional (página atual, dados relevantes)
        
    Returns:
        Resposta contextualizada
    """
    from .knowledge_base import search_knowledge, get_contextual_help, FAQ_COMUM
    
    # Primeiro, tenta encontrar na base de conhecimento
    knowledge_results = search_knowledge(question)
    context_help = get_contextual_help(context or "")
    
    # Constrói contexto enriquecido
    knowledge_context = ""
    if knowledge_results:
        knowledge_context += "\nInformações relevantes da base de conhecimento:\n"
        for topic, content in knowledge_results[:3]:  # Limita a 3 resultados
            knowledge_context += f"- {topic}: {str(content)[:200]}...\n"
    
    if context_help:
        knowledge_context += f"\nContexto da página atual: {str(context_help)[:300]}...\n"
    
    # Adiciona FAQs comuns se relevante
    for faq in FAQ_COMUM:
        if any(word in question.lower() for word in faq["pergunta"].lower().split()):
            knowledge_context += f"\nFAQ relacionada: {faq['pergunta']} - {faq['resposta']}\n"
            break
    
    system_message = f"""
    Você é um assistente especializado no sistema InventarioPro, um sistema de gestão de inventário para eventos.
    
    O sistema possui:
    - Gestão de Eventos (criação, edição, datas, locais)
    - Gestão de Produtos (cadastro, preços, categorias)
    - Controle de Estoque (geral e por sala/evento)
    - Sistema de Propostas (orçamentos para eventos)
    - Dashboard com estatísticas
    - Assistente de IA integrado
    
    Funcionalidades principais:
    - Criar eventos com salas associadas
    - Cadastrar produtos com preços em BRL
    - Controlar estoque geral e por localização
    - Gerar propostas comerciais
    - Visualizar estatísticas no dashboard
    - Usar IA para melhorar descrições e sugerir produtos
    
    {knowledge_context}
    
    Responda de forma clara e prática, focando em como usar o sistema. Use as informações da base de conhecimento quando disponíveis.
    """
    
    context_info = f"\nContexto atual: {context}" if context else ""
    prompt = f"Pergunta: {question}{context_info}"
    
    return send_chat(prompt, system_message=system_message, temperature=0.2, max_tokens=400)

def generate_report_summary(data: dict, report_type: str) -> str:
    """
    Gera resumos e insights para relatórios.
    
    Args:
        data: Dados do relatório
        report_type: Tipo de relatório (eventos, estoque, propostas, etc.)
        
    Returns:
        Resumo com insights
    """
    system_message = """
    Você é um analista de dados especializado em inventário e eventos.
    Analise os dados fornecidos e gere insights úteis e recomendações práticas.
    Seja objetivo e foque em informações acionáveis.
    """
    
    prompt = f"""
    Analise estes dados de {report_type} e gere um resumo com insights:
    
    {data}
    
    Forneça:
    1. Resumo dos principais números
    2. Tendências identificadas
    3. Recomendações práticas
    4. Alertas importantes (se houver)
    """
    
    return send_chat(prompt, system_message=system_message, temperature=0.3, max_tokens=400)

def suggest_automation_text(context: str, text_type: str) -> str:
    """
    Gera textos automatizados para diferentes contextos.
    
    Args:
        context: Contexto da situação
        text_type: Tipo de texto (email, notificacao, instrucao, etc.)
        
    Returns:
        Texto sugerido
    """
    system_message = """
    Você é um assistente de comunicação profissional.
    Gere textos claros, profissionais e adequados ao contexto do sistema de inventário.
    """
    
    prompt = f"""
    Gere um {text_type} profissional para esta situação:
    
    Contexto: {context}
    
    O texto deve ser:
    - Claro e objetivo
    - Profissional mas amigável
    - Adequado ao contexto de gestão de inventário
    """
    
    return send_chat(prompt, system_message=system_message, temperature=0.4, max_tokens=200)

def format_event_name(name: str) -> str:
    """
    Remove espaços das extremidades e coloca em Title Case.
    Ex: "  reunião anual  " → "Reunião Anual"
    """
    return name.strip().title()

def calculate_stock_total(quantities: list[int]) -> int:
    """
    Soma uma lista de quantidades.
    Ex: [3, 5, 2] → 10
    """
    return sum(quantities)

def slugify_title(title: str) -> str:
    """
    Gera um slug em lowercase, trocando tudo que não for letra/número por hífen.
    Ex: "Meu Evento #1!" → "meu-evento-1"
    """
    # subtitui tudo que não seja a-z ou 0-9 por hífen
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
    # remove hífens extras nas pontas
    return slug.strip('-')