# camarim/management/commands/import_full_legacy.py
import json, os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from camarim.models import Categoria, Produto, Estoque

LEGACY_FIXTURE = "legacy_data_utf8.json"
# pasta onde você copiou o 'media' antigo
LEGACY_MEDIA_ROOT = os.path.join(settings.BASE_DIR, "legacy_media")

class Command(BaseCommand):
    help = "Importa Categorias, Produtos (com imagem) e Estoque da base legacy"

    def handle(self, *args, **opts):
        # 1) Carrega o JSON legado
        with open(LEGACY_FIXTURE, encoding="utf-8") as f:
            data = json.load(f)

        # 2) Importa Categorias
        for obj in data:
            if obj["model"] == "camarim.categoria":
                nome = obj["fields"]["nome"]
                Categoria.objects.get_or_create(nome=nome)

        # 3) Importa Produtos + Imagem
        for obj in data:
            if obj["model"] == "camarim.produto":
                f = obj["fields"]
                cat = Categoria.objects.filter(nome=f["categoria"][1] if isinstance(f["categoria"], list) else f["categoria"]).first()
                prod, _ = Produto.objects.get_or_create(
                    nome=f["nome"],
                    defaults={
                        "preco": f["preco"],
                        "categoria": cat,
                        "descricao": f.get("descricao", "") or "",
                    }
                )
                # Se você re-adicionou o ImageField a Produto, setar aqui:
                imagem_path = f.get("imagem")
                if imagem_path:
                    abs_path = os.path.join(LEGACY_MEDIA_ROOT, imagem_path)
                    if os.path.isfile(abs_path):
                        with open(abs_path, "rb") as imgf:
                            prod.imagem.save(
                                os.path.basename(imagem_path),
                                File(imgf),
                                save=True
                            )

        # 4) Importa Estoque (quantidade) no modelo Estoque
        for obj in data:
            if obj["model"] == "camarim.produto":
                f = obj["fields"]
                nome = f["nome"]
                qtd = f.get("quantidade", 0)
                try:
                    prod = Produto.objects.get(nome=nome)
                    Estoque.objects.update_or_create(
                        produto=prod,
                        defaults={"quantidade": qtd}
                    )
                except Produto.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Produto não encontrado: {nome}"))

        # 5) Importa Usuários
        User = get_user_model()
        for obj in data:
            if obj["model"] == "auth.user":
                u = obj["fields"]
                if not User.objects.filter(username=u["username"]).exists():
                    User.objects.create(
                        username=u["username"],
                        email=u["email"],
                        password=u["password"],  # hash preservado
                        is_active=u["is_active"]
                    )

        self.stdout.write(self.style.SUCCESS("Importação completa!"))
