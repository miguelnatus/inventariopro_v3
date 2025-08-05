# Em camarim/views.py, adicione ao final:
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sala
from .forms import EstoqueSalaForm

class SalaDetailView(LoginRequiredMixin, View):
    template_name = 'camarim/sala_detail.html'

    def get(self, request, evento_pk, pk):
        sala = get_object_or_404(Sala, pk=pk, evento_id=evento_pk)
        form = EstoqueSalaForm()
        itens = sala.estoque_salas.all()
        return render(request, self.template_name, {
            'sala': sala, 'form_estoque': form, 'itens': itens
        })

    def post(self, request, evento_pk, pk):
        sala = get_object_or_404(Sala, pk=pk, evento_id=evento_pk)
        form = EstoqueSalaForm(request.POST)
        if form.is_valid():
            estoque = form.save(commit=False)
            estoque.sala = sala
            estoque.save()
        return self.get(request, evento_pk, pk)
