# camarim/tests/test_utils.py

import pytest

# importe aqui as funções que você quer testar
from camarim.utils import (
    format_event_name,
    calculate_stock_total,
    slugify_title,
)

def test_format_event_name_trims_and_titlecases():
    assert format_event_name("  reunião anual  ") == "Reunião Anual"

def test_calculate_stock_total_positive():
    # supondo que calculate_stock_total receba lista de quantidades
    assert calculate_stock_total([3, 5, 2]) == 10

def test_slugify_title_handles_special_chars():
    assert slugify_title("Meu Evento #1!") == "meu-evento-1"