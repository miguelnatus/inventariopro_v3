import pytest
from camarim.forms import EventoForm

def test_evento_form_valido():
    data = {"nome": "Teste", "data": "2025-08-10"}
    form = EventoForm(data=data)
    assert form.is_valid()

def test_evento_form_invalido_sem_nome():
    form = EventoForm(data={"nome": "", "data": "2025-08-10"})
    assert not form.is_valid()
    assert "nome" in form.errors