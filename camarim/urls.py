from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import (
    HomeRedirectView, DashboardView,
    EventoListView,EventoCreateView,EventoUpdateView,EventoDeleteView,
    SalaListView,SalaCreateView,SalaUpdateView,SalaDeleteView,
    ProdutoListView,ProdutoCreateView,ProdutoUpdateView,ProdutoDeleteView,
    EstoqueListView,EstoqueCreateView,EstoqueUpdateView,EstoqueDeleteView,
    EstoqueSalaListView,EstoqueSalaCreateView,EstoqueSalaUpdateView,EstoqueSalaDeleteView,
    PropostaListView,PropostaCreateView,PropostaDetailView,PropostaDeleteView,HelpView,RegisterView, CustomLoginView, LogoutGetView
)
from .ai_views import (
    AIAssistantView, enhance_event_form, product_suggestions, 
    chat_faq, get_context_help
)
from .reports_views import ReportsView, generate_automation_text, export_report


app_name = 'camarim'
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    # login/logout
    path('login/', CustomLoginView.as_view(), name='login'),
     path('logout/',   LogoutGetView.as_view(),  name='logout'),

    # home
    path('', HomeRedirectView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('painel/', RedirectView.as_view(pattern_name='camarim:dashboard'), name='painel'),
    # eventos
    path('painel/eventos/', EventoListView.as_view(),     name='evento_list'),
    path('painel/eventos/criar/', EventoCreateView.as_view(), name='evento_create'),
    path('painel/eventos/<int:pk>/editar/', EventoUpdateView.as_view(), name='evento_edit'),
    path('painel/eventos/<int:pk>/excluir/',EventoDeleteView.as_view(),name='evento_delete'),

    # salas
    path('painel/eventos/<int:evento_pk>/salas/',     SalaListView.as_view(),   name='sala_list'),
    path('painel/eventos/<int:evento_pk>/salas/criar/', SalaCreateView.as_view(), name='sala_create'),
    path('painel/eventos/<int:evento_pk>/salas/<int:pk>/editar/', SalaUpdateView.as_view(), name='sala_edit'),
    path('painel/eventos/<int:evento_pk>/salas/<int:pk>/excluir/',SalaDeleteView.as_view(),name='sala_delete'),

    # produtos
    path('painel/produtos/',     ProdutoListView.as_view(),   name='produto_list'),
    path('painel/produtos/criar/', ProdutoCreateView.as_view(), name='produto_create'),
    path('painel/produtos/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto_edit'),
    path('painel/produtos/<int:pk>/excluir/',ProdutoDeleteView.as_view(),name='produto_delete'),

    # estoque geral
    path('painel/estoque/',      EstoqueListView.as_view(),    name='estoque_list'),
    path('painel/estoque/criar/',EstoqueCreateView.as_view(),  name='estoque_create'),
    path('painel/estoque/<int:pk>/editar/',EstoqueUpdateView.as_view(), name='estoque_edit'),
    path('painel/estoque/<int:pk>/excluir/',EstoqueDeleteView.as_view(),name='estoque_delete'),

    # estoque em sala
    path('painel/eventos/<int:evento_pk>/salas/<int:sala_pk>/estoque/',         EstoqueSalaListView.as_view(),   name='estoque_sala_list'),
    path('painel/eventos/<int:evento_pk>/salas/<int:sala_pk>/estoque/criar/',   EstoqueSalaCreateView.as_view(), name='estoque_sala_create'),
    path('painel/eventos/<int:evento_pk>/salas/<int:sala_pk>/estoque/<int:pk>/editar/',EstoqueSalaUpdateView.as_view(),name='estoque_sala_edit'),
    path('painel/eventos/<int:evento_pk>/salas/<int:sala_pk>/estoque/<int:pk>/excluir/',EstoqueSalaDeleteView.as_view(),name='estoque_sala_delete'),

    # propostas
    path('painel/propostas/', PropostaListView.as_view(), name='proposta_list'),
    path('painel/propostas/criar/', PropostaCreateView.as_view(), name='proposta_create'),
    path('painel/propostas/<int:pk>/', PropostaDetailView.as_view(), name='proposta_detail'),
    path('painel/propostas/<int:pk>/deletar/', PropostaDeleteView.as_view(), name='proposta_delete'),
    
    # AI Assistant endpoints
    path('api/ai/', AIAssistantView.as_view(), name='ai_assistant'),
    path('api/ai/enhance-event/', enhance_event_form, name='enhance_event'),
    path('api/ai/suggest-products/', product_suggestions, name='suggest_products'),
    path('api/ai/chat-faq/', chat_faq, name='chat_faq'),
    path('api/ai/context-help/', get_context_help, name='context_help'),
    
    # Reports endpoints
    path('painel/relatorios/', ReportsView.as_view(), name='reports'),
    path('api/reports/automation-text/', generate_automation_text, name='generate_automation_text'),
    path('api/reports/export/', export_report, name='export_report'),

        # rota da Central de Ajuda
    path('ajuda/', HelpView.as_view(), name='help'),
]
