import pytest
from camarim.models import Evento, Sala

@pytest.mark.django_db
def test_criar_evento_e_str():
    ev = Evento.objects.create(nome="Festa Teste")
    assert str(ev) == "Festa Teste"

@pytest.mark.django_db
def test_sala_relacionada_ao_evento():
    ev = Evento.objects.create(nome="EV")
    sala = Sala.objects.create(evento=ev, nome="Sala A")
    assert sala.evento == ev
    assert "Sala A" in str(sala)
