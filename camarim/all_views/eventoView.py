from camarim.models import Evento
from camarim.forms  import EventoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ( ListView, CreateView, UpdateView, DeleteView )   
from django.urls import reverse_lazy

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