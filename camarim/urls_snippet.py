# Em camarim/urls.py, importe:
from .views import SalaDetailView

# E acrescente nas rotas de Salas:
path('painel/eventos/<int:evento_pk>/salas/<int:pk>/', SalaDetailView.as_view(), name='sala_detail'),
