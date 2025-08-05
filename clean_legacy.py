# clean_legacy.py
import json

IN_FILE  = "legacy_data_utf8.json"
OUT_FILE = "legacy_clean.json"

with open(IN_FILE, encoding="utf-8") as f:
    data = json.load(f)

clean = []
for obj in data:
    if obj["model"] == "camarim.produto":
        # remove os campos que não existem mais
        obj["fields"].pop("imagem", None)
        obj["fields"].pop("quantidade", None)
    clean.append(obj)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)

print(f"Fixture limpa escrita em {OUT_FILE}")
