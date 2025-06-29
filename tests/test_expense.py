from aitana.utils.expenses import parse_expense


def test_parse_expense():
    text = "Hola soy Alberto y hoy me he gastado 15 euros en Mercadona comprando fruta."
    exp = parse_expense(text)
    assert exp and exp["name"] == "Alberto" and abs(exp["amount"] - 15) < 0.01
