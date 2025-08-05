# reencode.py
import sys

# ajuste estes nomes se necessário
input_file  = 'legacy_data.json'
output_file = 'legacy_data_utf8.json'

# step 1: detecte ou assuma o encoding original (provavelmente utf-16)
with open(input_file, 'r', encoding='utf-16') as f:
    data = f.read()

# step 2: grave em UTF-8 sem BOM
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(data)

print(f"Escrito {output_file} em UTF-8.")