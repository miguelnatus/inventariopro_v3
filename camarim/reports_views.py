from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from datetime import datetime, timedelta
from .models import Evento, Produto, Estoque, Proposta, Categoria
from .utils import generate_report_summary, suggest_automation_text

@method_decorator(login_required, name='dispatch')
class ReportsView(View):
    """View para relatórios inteligentes"""
    
    def get(self, request):
        """Página principal de relatórios"""
        context = {
            'total_eventos': Evento.objects.count(),
            'total_produtos': Produto.objects.count(),
            'total_propostas': Proposta.objects.count(),
            'valor_total_propostas': Proposta.objects.aggregate(
                total=Sum('valor_total')
            )['total'] or 0,
        }
        return render(request, 'camarim/reports.html', context)
    
    def post(self, request):
        """Gera relatórios via AJAX"""
        try:
            data = json.loads(request.body)
            report_type = data.get('type', 'geral')
            
            if report_type == 'eventos':
                return self.generate_events_report(data)
            elif report_type == 'produtos':
                return self.generate_products_report(data)
            elif report_type == 'estoque':
                return self.generate_inventory_report(data)
            elif report_type == 'propostas':
                return self.generate_proposals_report(data)
            elif report_type == 'financeiro':
                return self.generate_financial_report(data)
            else:
                return self.generate_general_report(data)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def generate_events_report(self, data):
        """Relatório de eventos"""
        # Dados básicos
        total_eventos = Evento.objects.count()
        eventos_com_data = Evento.objects.exclude(data_inicial__isnull=True).count()
        eventos_recentes = Evento.objects.filter(
            data_inicial__gte=datetime.now() - timedelta(days=30)
        ).count()
        
        # Eventos por mês
        eventos_por_mes = Evento.objects.extra(
            select={'mes': "strftime('%%Y-%%m', data_inicial)"}
        ).values('mes').annotate(count=Count('id')).order_by('mes')
        
        report_data = {
            'total_eventos': total_eventos,
            'eventos_com_data': eventos_com_data,
            'eventos_recentes': eventos_recentes,
            'eventos_por_mes': list(eventos_por_mes),
            'taxa_eventos_com_data': (eventos_com_data / total_eventos * 100) if total_eventos > 0 else 0
        }
        
        # Gerar insights com IA
        summary = generate_report_summary(report_data, 'eventos')
        
        return JsonResponse({
            'success': True,
            'data': report_data,
            'summary': summary,
            'type': 'eventos'
        })
    
    def generate_products_report(self, data):
        """Relatório de produtos"""
        total_produtos = Produto.objects.count()
        produtos_com_categoria = Produto.objects.exclude(categoria__isnull=True).count()
        
        # Produtos por categoria
        produtos_por_categoria = Categoria.objects.annotate(
            total_produtos=Count('produtos')
        ).values('nome', 'total_produtos').order_by('-total_produtos')
        
        # Preços médios
        preco_medio = Produto.objects.aggregate(
            media=Avg('preco')
        )['media'] or 0
        
        # Produtos mais caros e mais baratos
        produto_mais_caro = Produto.objects.order_by('-preco').first()
        produto_mais_barato = Produto.objects.order_by('preco').first()
        
        report_data = {
            'total_produtos': total_produtos,
            'produtos_com_categoria': produtos_com_categoria,
            'produtos_por_categoria': list(produtos_por_categoria),
            'preco_medio': float(preco_medio),
            'produto_mais_caro': {
                'nome': produto_mais_caro.nome if produto_mais_caro else '',
                'preco': float(produto_mais_caro.preco) if produto_mais_caro else 0
            },
            'produto_mais_barato': {
                'nome': produto_mais_barato.nome if produto_mais_barato else '',
                'preco': float(produto_mais_barato.preco) if produto_mais_barato else 0
            }
        }
        
        summary = generate_report_summary(report_data, 'produtos')
        
        return JsonResponse({
            'success': True,
            'data': report_data,
            'summary': summary,
            'type': 'produtos'
        })
    
    def generate_inventory_report(self, data):
        """Relatório de estoque"""
        # Produtos com baixo estoque
        produtos_baixo_estoque = Produto.objects.filter(
            estoques__quantidade__lt=10
        ).distinct().count()
        
        # Estoque total
        estoque_total = Estoque.objects.aggregate(
            total=Sum('quantidade')
        )['total'] or 0
        
        # Produtos sem estoque
        produtos_sem_estoque = Produto.objects.filter(
            estoques__quantidade=0
        ).distinct().count()
        
        # Top produtos por quantidade
        top_produtos_estoque = Estoque.objects.select_related('produto').values(
            'produto__nome'
        ).annotate(
            total_quantidade=Sum('quantidade')
        ).order_by('-total_quantidade')[:5]
        
        report_data = {
            'produtos_baixo_estoque': produtos_baixo_estoque,
            'estoque_total': estoque_total,
            'produtos_sem_estoque': produtos_sem_estoque,
            'top_produtos_estoque': list(top_produtos_estoque),
            'alerta_critico': produtos_sem_estoque > 0
        }
        
        summary = generate_report_summary(report_data, 'estoque')
        
        return JsonResponse({
            'success': True,
            'data': report_data,
            'summary': summary,
            'type': 'estoque'
        })
    
    def generate_proposals_report(self, data):
        """Relatório de propostas"""
        total_propostas = Proposta.objects.count()
        valor_total = Proposta.objects.aggregate(
            total=Sum('valor_total')
        )['total'] or 0
        
        valor_medio = Proposta.objects.aggregate(
            media=Avg('valor_total')
        )['media'] or 0
        
        # Propostas por mês
        propostas_por_mes = Proposta.objects.extra(
            select={'mes': "strftime('%%Y-%%m', data_criacao)"}
        ).values('mes').annotate(
            count=Count('id'),
            valor_total=Sum('valor_total')
        ).order_by('mes')
        
        # Top eventos por valor de propostas
        top_eventos = Proposta.objects.select_related('evento').values(
            'evento__nome'
        ).annotate(
            total_valor=Sum('valor_total'),
            total_propostas=Count('id')
        ).order_by('-total_valor')[:5]
        
        report_data = {
            'total_propostas': total_propostas,
            'valor_total': float(valor_total),
            'valor_medio': float(valor_medio),
            'propostas_por_mes': list(propostas_por_mes),
            'top_eventos': list(top_eventos)
        }
        
        summary = generate_report_summary(report_data, 'propostas')
        
        return JsonResponse({
            'success': True,
            'data': report_data,
            'summary': summary,
            'type': 'propostas'
        })
    
    def generate_financial_report(self, data):
        """Relatório financeiro"""
        # Valor total das propostas
        valor_total_propostas = Proposta.objects.aggregate(
            total=Sum('valor_total')
        )['total'] or 0
        
        # Valor médio por proposta
        valor_medio_proposta = Proposta.objects.aggregate(
            media=Avg('valor_total')
        )['media'] or 0
        
        # Valor total do inventário (produtos * preço)
        valor_inventario = 0
        for produto in Produto.objects.all():
            quantidade_total = produto.estoques.aggregate(
                total=Sum('quantidade')
            )['total'] or 0
            valor_inventario += float(produto.preco) * quantidade_total
        
        # Propostas recentes (últimos 30 dias)
        propostas_recentes = Proposta.objects.filter(
            data_criacao__gte=datetime.now() - timedelta(days=30)
        ).aggregate(
            total=Sum('valor_total'),
            count=Count('id')
        )
        
        report_data = {
            'valor_total_propostas': float(valor_total_propostas),
            'valor_medio_proposta': float(valor_medio_proposta),
            'valor_inventario': valor_inventario,
            'propostas_recentes': {
                'valor': float(propostas_recentes['total'] or 0),
                'quantidade': propostas_recentes['count']
            }
        }
        
        summary = generate_report_summary(report_data, 'financeiro')
        
        return JsonResponse({
            'success': True,
            'data': report_data,
            'summary': summary,
            'type': 'financeiro'
        })
    
    def generate_general_report(self, data):
        """Relatório geral do sistema"""
        report_data = {
            'total_eventos': Evento.objects.count(),
            'total_produtos': Produto.objects.count(),
            'total_propostas': Proposta.objects.count(),
            'valor_total_propostas': float(Proposta.objects.aggregate(
                total=Sum('valor_total')
            )['total'] or 0),
            'produtos_baixo_estoque': Produto.objects.filter(
                estoques__quantidade__lt=10
            ).distinct().count(),
            'eventos_recentes': Evento.objects.filter(
                data_inicial__gte=datetime.now() - timedelta(days=30)
            ).count()
        }
        
        summary = generate_report_summary(report_data, 'geral')
        
        return JsonResponse({
            'success': True,
            'data': report_data,
            'summary': summary,
            'type': 'geral'
        })

@login_required
@csrf_exempt
def generate_automation_text(request):
    """Endpoint para geração de textos automatizados"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        context = data.get('context', '')
        text_type = data.get('text_type', 'geral')
        
        if not context:
            return JsonResponse({'error': 'Contexto é obrigatório'}, status=400)
        
        generated_text = suggest_automation_text(context, text_type)
        
        return JsonResponse({
            'success': True,
            'text': generated_text,
            'type': text_type
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def export_report(request):
    """Exporta relatório em diferentes formatos"""
    report_type = request.GET.get('type', 'geral')
    format_type = request.GET.get('format', 'json')
    
    # Aqui você pode implementar exportação para PDF, Excel, etc.
    # Por enquanto, retorna JSON
    
    return JsonResponse({
        'message': f'Exportação de relatório {report_type} em formato {format_type} será implementada em breve'
    })

