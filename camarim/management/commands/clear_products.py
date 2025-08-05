from django.core.management.base import BaseCommand
from camarim.models import Produto

class Command(BaseCommand):
    help = "Remove todos os produtos da tabela camarim_produto"

    def handle(self, *args, **options):
        count, _ = Produto.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            f"✅ Produtos apagados: {count} registros."
        ))