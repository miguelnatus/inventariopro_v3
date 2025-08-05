# camarim/legacy_models.py
from django.db import models

class OldProduto(models.Model):
    id         = models.IntegerField(primary_key=True)
    nome       = models.CharField(max_length=200)
    preco      = models.DecimalField(max_digits=14, decimal_places=2)
    quantidade = models.IntegerField()
    imagem     = models.CharField(max_length=200, blank=True, null=True)
    # Se precisar de categoria, adicione também:
    # categoria_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camarim_produto'
        app_label = 'camarim'