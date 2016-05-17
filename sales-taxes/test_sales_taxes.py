from sales_taxes import *
from io import StringIO

tests = [
# test 1
("""
1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85
""",
 """\
1 book: 12.49
1 music CD: 16.49
1 chocolate bar: 0.85
Sales Taxes: 1.50
Total: 29.83
"""),

# test 2
("""
1 imported box of chocolates at 10.00
1 imported bottle of perfume at 47.50
""",
 """\
1 imported box of chocolates: 10.50
1 imported bottle of perfume: 54.65
Sales Taxes: 7.65
Total: 65.15
"""),

# test 3
( """
1 imported bottle of perfume at 27.99
1 bottle of perfume at 18.99
1 packet of headache pills at 9.75
1 box of imported chocolates at 11.25
""",
"""\
1 imported bottle of perfume: 32.19
1 bottle of perfume: 20.89
1 packet of headache pills: 9.75
1 imported box of chocolates: 11.85
Sales Taxes: 6.70
Total: 74.68
""")
]


def test_round005():
    assert round005(Decimal("0.01")) == Decimal("0.00")
    assert round005(Decimal("0.93")) == Decimal("0.95")
    assert round005(Decimal("0.65")) == Decimal("0.65")
    assert round005(Decimal("0.68")) == Decimal("0.70")
    assert round005(Decimal("0.67")) == Decimal("0.65")


def test_main():
    for inpt, expected in tests:
        out = StringIO()
        process_input(inpt, stream=out)
        assert out.getvalue() == expected
