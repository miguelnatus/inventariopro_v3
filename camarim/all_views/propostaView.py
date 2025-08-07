from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ( ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView )
from django.urls import reverse_lazy
from camarim.models import Proposta
from camarim.forms  import PropostaForm, ItemPropostaFormSet

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

class PropostaUpdateView(UpdateView):
    model = Proposta
    form_class = PropostaForm
    template_name = 'camarim/proposta_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ItemPropostaFormSet(instance=self.object)
        return self.render_to_response({'form':form,'formset':formset,'proposta':self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ItemPropostaFormSet(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('proposta_detail', pk=self.object.pk)
        return self.render_to_response({'form':form,'formset':formset,'proposta':self.object})


class DescritivoView(TemplateView):
    template_name = 'camarim/proposta_descritivo.html'

    def get_context_data(self, **kwargs):
        pk = kwargs['pk']
        prop = get_object_or_404(Proposta, pk=pk)
        # agrupa items por sala
        salas = {}
        for item in prop.itens.all().order_by('sala__nome'):
            salas.setdefault(item.sala, []).append(item)
        return {'proposta': prop, 'salas': salas}