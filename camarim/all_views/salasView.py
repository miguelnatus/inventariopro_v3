from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ( ListView, CreateView, UpdateView, DeleteView, FormView )
from django.urls import reverse_lazy
from camarim.models import Sala, Evento
from camarim.forms  import SalaForm, SalaReplicateForm

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
