import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_evento_list_view(client, django_user_model):
    # cria um usuário e faz login
    user = django_user_model.objects.create_user("u", "u@u.com", "pwd")
    client.login(username="u", password="pwd")

    url = reverse("camarim:evento_list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert "eventos" in resp.context
