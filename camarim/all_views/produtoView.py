from camarim.models import Produto, Estoque
# from camarim.views import HomeRedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ( ListView, CreateView, UpdateView, DeleteView )
from django.urls import reverse_lazy
from django.db.models import Sum, Value
from camarim.forms  import ProdutoForm, EstoqueForm
from django.db.models.functions import Coalesce

# class HomeRedirectView(RedirectView):
#     pattern_name = 'camarim:dashboard'

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'camarim/produto_list.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        # Anota 'stock' como soma das quantidades em Estoque, ou 0 se none
        qs = super().get_queryset().annotate(
            stock=Coalesce(Sum('estoques__quantidade'), Value(0))
        )
        return qs
    
class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model=Produto; form_class=ProdutoForm; template_name='camarim/produto_form.html'
    success_url=reverse_lazy('camarim:produto_list')
class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model=Produto; form_class=ProdutoForm; template_name='camarim/produto_form.html'
    success_url=reverse_lazy('camarim:produto_list')
class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model=Produto; template_name='camarim/produto_confirm_delete.html'
    success_url=reverse_lazy('camarim:produto_list')

# — Estoque Geral —
class EstoqueListView(LoginRequiredMixin, ListView):
    model=Estoque; template_name='camarim/estoque_list.html'; context_object_name='estoque_items'
class EstoqueCreateView(LoginRequiredMixin, CreateView):
    model=Estoque; form_class=EstoqueForm; template_name='camarim/estoque_form.html'
    success_url=reverse_lazy('camarim:estoque_list')
class EstoqueUpdateView(LoginRequiredMixin, UpdateView):
    model=Estoque; form_class=EstoqueForm; template_name='camarim/estoque_form.html'
    success_url=reverse_lazy('camarim:estoque_list')
class EstoqueDeleteView(LoginRequiredMixin, DeleteView):
    model=Estoque; template_name='camarim/estoque_confirm_delete.html'
    success_url=reverse_lazy('camarim:estoque_list')
