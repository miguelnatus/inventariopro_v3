# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views import View
# from .utils import (
#     generate_event_description, 
#     suggest_products_categories, 
#     answer_faq, 
#     generate_report_summary,
#     suggest_automation_text
# )

# @method_decorator(login_required, name='dispatch')
# @method_decorator(csrf_exempt, name='dispatch')
# class AIAssistantView(View):
#     """View base para funcionalidades do assistente de IA"""
    
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             action = data.get('action')
            
#             if action == 'generate_event':
#                 return self.generate_event_description(data)
#             elif action == 'suggest_products':
#                 return self.suggest_products(data)
#             elif action == 'faq':
#                 return self.answer_faq(data)
#             elif action == 'generate_report':
#                 return self.generate_report(data)
#             elif action == 'automation_text':
#                 return self.automation_text(data)
#             else:
#                 return JsonResponse({'error': 'Ação não reconhecida'}, status=400)
                
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'JSON inválido'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
    
#     def generate_event_description(self, data):
#         """Gera descrição de evento baseada em rascunho"""
#         draft = data.get('draft', '')
#         if not draft:
#             return JsonResponse({'error': 'Rascunho é obrigatório'}, status=400)
        
#         result = generate_event_description(draft)
#         return JsonResponse({
#             'success': True,
#             'data': result
#         })
    
#     def suggest_products(self, data):
#         """Sugere produtos e categorias"""
#         description = data.get('description', '')
#         if not description:
#             return JsonResponse({'error': 'Descrição é obrigatória'}, status=400)
        
#         result = suggest_products_categories(description)
#         return JsonResponse({
#             'success': True,
#             'data': result
#         })
    
#     def answer_faq(self, data):
#         """Responde perguntas sobre o sistema"""
#         question = data.get('question', '')
#         context = data.get('context', '')
        
#         if not question:
#             return JsonResponse({'error': 'Pergunta é obrigatória'}, status=400)
        
#         answer = answer_faq(question, context)
#         return JsonResponse({
#             'success': True,
#             'answer': answer
#         })
    
#     def generate_report(self, data):
#         """Gera resumo de relatório"""
#         report_data = data.get('data', {})
#         report_type = data.get('type', 'geral')
        
#         if not report_data:
#             return JsonResponse({'error': 'Dados do relatório são obrigatórios'}, status=400)
        
#         summary = generate_report_summary(report_data, report_type)
#         return JsonResponse({
#             'success': True,
#             'summary': summary
#         })
    
#     def automation_text(self, data):
#         """Gera texto automatizado"""
#         context = data.get('context', '')
#         text_type = data.get('text_type', 'geral')
        
#         if not context:
#             return JsonResponse({'error': 'Contexto é obrigatório'}, status=400)
        
#         text = suggest_automation_text(context, text_type)
#         return JsonResponse({
#             'success': True,
#             'text': text
#         })

# @login_required
# @csrf_exempt
# @require_http_methods(["POST"])
# def enhance_event_form(request):
#     """
#     Endpoint específico para melhorar formulários de eventos
#     """
#     try:
#         data = json.loads(request.body)
#         draft = data.get('draft', '')
        
#         if not draft:
#             return JsonResponse({'error': 'Rascunho é obrigatório'}, status=400)
        
#         # Gera descrição melhorada
#         enhanced = generate_event_description(draft)
        
#         return JsonResponse({
#             'success': True,
#             'enhanced': enhanced
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# @login_required
# @csrf_exempt
# @require_http_methods(["POST"])
# def product_suggestions(request):
#     """
#     Endpoint específico para sugestões de produtos
#     """
#     try:
#         data = json.loads(request.body)
#         description = data.get('description', '')
        
#         if not description:
#             return JsonResponse({'error': 'Descrição é obrigatória'}, status=400)
        
#         # Gera sugestões
#         suggestions = suggest_products_categories(description)
        
#         return JsonResponse({
#             'success': True,
#             'suggestions': suggestions
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# @login_required
# @csrf_exempt
# @require_http_methods(["POST"])
# def chat_faq(request):
#     """
#     Endpoint para chat de FAQ
#     """
#     try:
#         data = json.loads(request.body)
#         question = data.get('question', '')
#         context = data.get('context', '')
        
#         if not question:
#             return JsonResponse({'error': 'Pergunta é obrigatória'}, status=400)
        
#         # Obtém resposta
#         answer = answer_faq(question, context)
        
#         return JsonResponse({
#             'success': True,
#             'answer': answer
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# @login_required
# def get_context_help(request):
#     """
#     Retorna ajuda contextual baseada na página atual
#     """
#     page = request.GET.get('page', '')
    
#     context_help = {
#         'dashboard': {
#             'title': 'Dashboard',
#             'description': 'Visão geral do sistema com estatísticas e ações rápidas',
#             'tips': [
#                 'Use os cards de estatísticas para ter uma visão geral',
#                 'Clique nas ações rápidas para criar novos itens',
#                 'Monitore produtos com baixo estoque'
#             ]
#         },
#         'eventos': {
#             'title': 'Gestão de Eventos',
#             'description': 'Criação e gerenciamento de eventos',
#             'tips': [
#                 'Use o assistente de IA para gerar descrições profissionais',
#                 'Adicione imagens para tornar os eventos mais atrativos',
#                 'Configure salas para cada evento'
#             ]
#         },
#         'produtos': {
#             'title': 'Gestão de Produtos',
#             'description': 'Cadastro e controle de produtos',
#             'tips': [
#                 'Use categorias para organizar produtos',
#                 'Defina preços em reais (BRL)',
#                 'Monitore o estoque regularmente'
#             ]
#         },
#         'propostas': {
#             'title': 'Sistema de Propostas',
#             'description': 'Criação de orçamentos para eventos',
#             'tips': [
#                 'Vincule propostas aos eventos correspondentes',
#                 'Use valores precisos para cálculos corretos',
#                 'Gere relatórios para análise'
#             ]
#         }
#     }
    
#     help_data = context_help.get(page, {
#         'title': 'InventarioPro',
#         'description': 'Sistema de gestão de inventário para eventos',
#         'tips': ['Use o menu lateral para navegar', 'Consulte a ajuda em cada seção']
#     })
    
#     return JsonResponse({
#         'success': True,
#         'help': help_data
#     })

