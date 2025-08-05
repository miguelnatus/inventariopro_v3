from django.db import models, transaction
from djmoney.models.fields import MoneyField
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self): return self.nome

class Produto(models.Model):
    def caminho_imagem(instance, filename):
        return f'{timezone.now().year}/{timezone.now().month}/{filename}'
    nome      = models.CharField(max_length=200)
    preco     = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='produtos')
    imagem    = models.ImageField(upload_to='produtos/%Y/%m', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    def __str__(self): return self.nome


class Estoque(models.Model):
    # produto    = models.ForeignKey(Produto, on_delete=models.CASCADE)
    produto    = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='estoques'      # agora você pode usar .estoques no reverse
    )
    quantidade = models.BigIntegerField()
    def __str__(self): return f"{self.produto.nome}: {self.quantidade}"

class Evento(models.Model):
    nome         = models.CharField(max_length=200)
    local        = models.CharField(max_length=200, blank=True)
    data_inicial = models.DateField(null=True, blank=True)
    data_final   = models.DateField(null=True, blank=True)
    descricao    = models.TextField(blank=True)
    imagem       = models.ImageField(upload_to='evento/%Y/%m', blank=True, null=True)
    def __str__(self): return self.nome

class Sala(models.Model):
    nome   = models.CharField(max_length=100)
    evento = models.ForeignKey(
        'Evento', 
        on_delete=models.CASCADE,
        related_name='salas'
    )
    def __str__(self):
        return f"{self.nome} ({self.evento.nome})"
    
    def replicar(self, novo_evento):
        """
        Clona esta sala para `novo_evento`, copiando todo o EstoqueSala
        associado e debitando do Estoque geral.
        """
        from .models import EstoqueSala, Estoque

        with transaction.atomic():
            # 1) Cria a nova sala
            sala_nova = Sala.objects.create(
                nome=self.nome,
                evento=novo_evento
            )
            # 2) Para cada item de estoque na sala original
            itens = EstoqueSala.objects.filter(sala=self)
            for item in itens:
                # 2a) Cria no estoque da nova sala
                EstoqueSala.objects.create(
                    sala=sala_nova,
                    produto=item.produto,
                    quantidade=item.quantidade
                )
                # 2b) Debita do estoque geral
                est_geral = Estoque.objects.get(produto=item.produto)
                est_geral.quantidade -= item.quantidade
                est_geral.save()

            return sala_nova

class EstoqueSala(models.Model):
    sala       = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='estoque_salas'
    )
    produto    = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='estoque_em_salas'
    )
    quantidade = models.BigIntegerField()

    class Meta:
        unique_together = ('sala', 'produto')

    def __str__(self):
        return f"{self.sala.nome}—{self.produto.nome}: {self.quantidade}"

class Proposta(models.Model):
    evento       = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='propostas'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    valor_total  = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    descricao    = models.TextField(blank=True)

    def __str__(self):
        return f"#{self.id} → {self.evento.nome} = R$ {self.valor_total}"
