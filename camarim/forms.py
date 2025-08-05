from django import forms
from django.forms import DateInput
from djmoney.forms.widgets import MoneyWidget
from .models import Evento, Sala, Produto, Estoque, EstoqueSala, Proposta

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields= ['nome','local','data_inicial','data_final','descricao','imagem']
        widgets = {
          'data_inicial': DateInput(attrs={'type':'date','class':'form-control'}),
          'data_final':   DateInput(attrs={'type':'date','class':'form-control'}),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields= ['nome']
        widgets={'nome': forms.TextInput(attrs={'class':'form-control'})}

class SalaReplicateForm(forms.Form):
    destino = forms.ModelChoiceField(
        queryset=Evento.objects.none(),      # vamos atribuir dinamicamente
        label="Evento de destino",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    def __init__(self, *args, eventos_origem=None, **kwargs):
        super().__init__(*args, **kwargs)
        if eventos_origem is not None:
            # só mostramos eventos diferentes do origem
            self.fields['destino'].queryset = Evento.objects.exclude(pk=eventos_origem)


class ProdutoForm(forms.ModelForm):
    quantidade = forms.IntegerField(
        label="Quantidade em Estoque",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0',
        })
    )

    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'descricao', 'quantidade']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto'
            }),
            'preco': MoneyWidget(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição (opcional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se já existe estoque, popula o inicial
        if self.instance.pk:
            est = Estoque.objects.filter(produto=self.instance).first()
            self.fields['quantidade'].initial = est.quantidade if est else 0

    def save(self, commit=True):
        produto = super().save(commit=commit)
        qtd = self.cleaned_data['quantidade']
        Estoque.objects.update_or_create(
            produto=produto,
            defaults={'quantidade': qtd}
        )
        return produto

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields= ['produto','quantidade']
        widgets={'quantidade': forms.NumberInput(attrs={'class':'form-control'})}

class EstoqueSalaForm(forms.ModelForm):
    class Meta:
        model = EstoqueSala
        fields= ['produto','quantidade']
        widgets={'quantidade': forms.NumberInput(attrs={'class':'form-control'})}

class PropostaForm(forms.ModelForm):
    class Meta:
        model = Proposta
        fields= ['evento','valor_total','descricao']
        widgets={'valor_total': forms.NumberInput(attrs={'class':'form-control'})}
