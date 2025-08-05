# camarim/management/commands/import_stock.py

from django.core.management.base import BaseCommand
from camarim.models import Produto, Estoque
from camarim.legacy_models import OldProduto

class Command(BaseCommand):
    help = "Importa estoque da base legacy"

    def handle(self, *args, **opts):
        total = 0
        for op in OldProduto.objects.using('legacy').all():
            prod = Produto.objects.filter(pk=op.id).first()
            if not prod:
                continue
            Estoque.objects.update_or_create(
                produto=prod,
                defaults={'quantidade': op.quantidade}
            )
            total += 1
        self.stdout.write(self.style.SUCCESS(f"{total} estoques importados."))