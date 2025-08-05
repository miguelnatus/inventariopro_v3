from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .ai_client import get_ai_client
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, IntegrityError
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, RedirectView, TemplateView, CreateView, FormView
)
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum , Value
from .models import Evento,Sala,Produto,Estoque,EstoqueSala,Proposta,Categoria
from .forms  import EventoForm, SalaForm, ProdutoForm, EstoqueForm, EstoqueSalaForm, PropostaForm, SalaReplicateForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Coalesce


class RegisterView(CreateView):
    """
    Tela de cadastro de novo usuário.
    """
    template_name = "registration/register.html"
    form_class    = UserCreationForm
    success_url   = reverse_lazy('camarim:login')

class CustomLoginView(LoginView):

    template_name = "registration/login.html"
    redirect_authenticated_user = True

class LogoutGetView(View):
    """
    Faz logout no GET ou POST e redireciona para a tela de login do InventarioPro.
    """
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        # chama o logout, independentemente do método
        logout(request)
        # redireciona para a sua rota de login
        return redirect(reverse_lazy('camarim:login'))

class HelpView(View):
    template_name = "help.html"

    def get(self, request):
        # página inicial com formulário de busca
        return render(request, self.template_name, {"answer": None})

    def post(self, request):
        query = request.POST.get("query", "").strip()
        answer = None
        if query:
            ai = get_ai_client()
            try:
                answer = ai.send_chat(query)
            except Exception as e:
                answer = "Desculpe, não consegui buscar a resposta agora."
                # opcional: logar e-insights
        return render(request, self.template_name, {
            "answer": answer,
            "query": query,
        })
    
class AIAjudaView(View):
    template_name = "ajuda.html"

    def get(self, request):
        # exibe o formulário inicial
        return render(request, self.template_name, {"query": "", "answer": None})

    def post(self, request):
        # pega a pergunta do usuário
        query = request.POST.get("query", "").strip()
        answer = None
        if query:
            client = get_ai_client()           # instancia OpenAIClient ou OpenRouterClient
            try:
                answer = client.send_chat(query)
            except Exception:
                answer = "Desculpe, não consegui buscar a resposta no momento."
        return render(request, self.template_name, {
            "query": query,
            "answer": answer,
        })

# raiz → redireciona ao dashboard
class HomeRedirectView(RedirectView):
    pattern_name = 'camarim:dashboard'

# Dashboard com estatísticas
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'camarim/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas gerais
        context['total_eventos'] = Evento.objects.count()
        context['total_produtos'] = Produto.objects.count()
        context['total_salas'] = Sala.objects.count()
        context['total_propostas'] = Proposta.objects.count()
        context['total_categorias'] = Categoria.objects.count()
        
        # Eventos recentes
        context['eventos_recentes'] = Evento.objects.order_by('-id')[:5]
        
        # Propostas recentes
        context['propostas_recentes'] = Proposta.objects.select_related('evento').order_by('-data_criacao')[:5]
        
        # Produtos com baixo estoque (menos de 10 unidades)
        context['produtos_baixo_estoque'] = Produto.objects.filter(
            estoques__quantidade__lt=10
        ).distinct()[:5]
        
        # Valor total das propostas
        valor_total_propostas = Proposta.objects.aggregate(
            total=Sum('valor_total')
        )['total'] or 0
        context['valor_total_propostas'] = valor_total_propostas
        
        # Estatísticas por categoria
        context['stats_categorias'] = Categoria.objects.annotate(
            total_produtos=Count('produtos')
        ).order_by('-total_produtos')[:5]
        
        return context

# — Eventos —
class EventoListView(LoginRequiredMixin, ListView):
    model=Evento; template_name='camarim/evento_list.html'; context_object_name='eventos'
class EventoCreateView(LoginRequiredMixin, CreateView):
    model=Evento; form_class=EventoForm; template_name='camarim/evento_form.html'
    success_url=reverse_lazy('camarim:evento_list')
class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model=Evento; form_class=EventoForm; template_name='camarim/evento_form.html'
    success_url=reverse_lazy('camarim:evento_list')
class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model=Evento; template_name='camarim/evento_confirm_delete.html'
    success_url=reverse_lazy('camarim:evento_list')

# — Salas —
class SalaListView(LoginRequiredMixin, ListView):
    model = Sala
    template_name = 'camarim/sala_list.html'
    context_object_name = 'salas'

    def get_queryset(self):
        return Sala.objects.filter(evento_id=self.kwargs['evento_pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['evento'] = Evento.objects.get(pk=self.kwargs['evento_pk'])
        # lista todos os eventos, exceto o atual, para o <select> de replicação
        ctx['eventos_todos'] = Evento.objects.exclude(pk=self.kwargs['evento_pk'])
        return ctx

class SalaCreateView(LoginRequiredMixin, CreateView):
    model=Sala; form_class=SalaForm; template_name='camarim/sala_form.html'
    def form_valid(self, form):
        form.instance.evento_id=self.kwargs['evento_pk']
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('camarim:sala_list', args=[self.kwargs['evento_pk']])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = Evento.objects.get(pk=self.kwargs['evento_pk'])
        return context

class SalaUpdateView(LoginRequiredMixin, UpdateView):
    model=Sala; form_class=SalaForm; template_name='camarim/sala_form.html'
    def get_success_url(self):
        return reverse_lazy('camarim:sala_list', args=[self.kwargs['evento_pk']])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = Evento.objects.get(pk=self.kwargs['evento_pk'])
        return context

class SalaDeleteView(LoginRequiredMixin, DeleteView):
    model=Sala; template_name='camarim/sala_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('camarim:sala_list', args=[self.kwargs['evento_pk']])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = Evento.objects.get(pk=self.kwargs['evento_pk'])
        return context

class SalaReplicateView(LoginRequiredMixin, FormView):
    template_name = 'camarim/sala_replicate.html'
    form_class    = SalaReplicateForm

    def dispatch(self, request, *args, **kwargs):
        # Carrega a sala e o evento de origem
        self.evento_origem = get_object_or_404(Evento, pk=kwargs['evento_pk'])
        self.sala_origem   = get_object_or_404(Sala,   pk=kwargs['sala_pk'], evento=self.evento_origem)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        # Diz ao form qual é o evento origem para filtrar o queryset
        kw['eventos_origem'] = self.evento_origem.pk
        return kw

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        # Passa pro template
        ctx['evento_origem'] = self.evento_origem
        ctx['sala_origem']   = self.sala_origem
        return ctx

    def form_valid(self, form):
        evento_dest = form.cleaned_data['destino']
        nova_sala = self.sala_origem.replicar(evento_dest)
        messages.success(
            self.request,
            f"Sala “{self.sala_origem.nome}” replicada para o evento “{evento_dest.nome}”."
        )
        return redirect('camarim:sala_list', evento_pk=evento_dest.pk)

# — Produtos —
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

# — Estoque por Sala —
class EstoqueSalaListView(LoginRequiredMixin, ListView):
    model = EstoqueSala
    template_name = 'camarim/estoque_sala_list.html'
    context_object_name = 'itens'

    def get_queryset(self):
        return EstoqueSala.objects.filter(
            sala_id=self.kwargs['sala_pk']
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sala'] = Sala.objects.get(pk=self.kwargs['sala_pk'])
        ctx['evento'] = Evento.objects.get(pk=self.kwargs['evento_pk'])
        return ctx


class EstoqueSalaCreateView(LoginRequiredMixin, CreateView):
    model = EstoqueSala
    form_class = EstoqueSalaForm
    template_name = 'camarim/estoque_sala_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.evento = get_object_or_404(Evento, pk=kwargs['evento_pk'])
        self.sala   = get_object_or_404(Sala,   pk=kwargs['sala_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        ctx['evento'] = self.evento
        ctx['sala']   = self.sala
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        produto       = form.cleaned_data['produto']
        qtd_para_sala = form.cleaned_data['quantidade']

        # 1) Reduz o estoque geral SEM checar limite
        estoque_geral = get_object_or_404(Estoque, produto=produto)
        estoque_geral.quantidade -= qtd_para_sala
        estoque_geral.save()

        # 2) Soma no estoque da sala
        sala_item, created = EstoqueSala.objects.get_or_create(
            sala=   self.sala,
            produto=produto,
            defaults={'quantidade': 0}
        )
        sala_item.quantidade += qtd_para_sala
        sala_item.save()

        # 3) Redireciona
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'camarim:estoque_sala_list',
            args=[self.evento.id, self.sala.id]
        )

class EstoqueSalaUpdateView(LoginRequiredMixin, UpdateView):
    model=EstoqueSala; form_class=EstoqueSalaForm; template_name='camarim/estoque_sala_form.html'
    def get_success_url(self):
        return reverse_lazy('camarim:estoque_sala_list',
                            args=[self.kwargs['evento_pk'],self.kwargs['sala_pk']])

class EstoqueSalaDeleteView(LoginRequiredMixin, DeleteView):
    model=EstoqueSala; template_name='camarim/estoque_sala_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('camarim:estoque_sala_list',
                            args=[self.kwargs['evento_pk'],self.kwargs['sala_pk']])

# — Propostas —
class PropostaListView(LoginRequiredMixin, ListView):
    model=Proposta; template_name='camarim/proposta_list.html'; context_object_name='propostas'
class PropostaCreateView(LoginRequiredMixin, CreateView):
    model=Proposta; form_class=PropostaForm; template_name='camarim/proposta_form.html'
    success_url=reverse_lazy('camarim:proposta_list')
class PropostaDetailView(LoginRequiredMixin, DetailView):
    model=Proposta; template_name='camarim/proposta_detail.html'
class PropostaDeleteView(LoginRequiredMixin, DeleteView):
    model=Proposta; template_name='camarim/proposta_confirm_delete.html'
    success_url=reverse_lazy('camarim:proposta_list')
