#!/usr/bin/env python3

"""
Calculates sales taxes. Please see README for more detailed description.
"""

from decimal import Decimal, ROUND_HALF_EVEN  # fixed point arithmetics
from sys import stdin, stdout
import re  # regexp routines


TAX_EXEMPT_MARKERS = "book chocolate food pills".split()
PATTERN = r"([0-9]+) (.+) at ([0-9]+\.[0-9]+)"
SALES_TAX = Decimal("0.10")    # 10% sales tax
IMPORT_DUTY = Decimal("0.05")  # 5% import duty
OUTPUT_FMT = "{count} {descr}: {price}"


class ParseError(Exception):
    """ Parsing errors raise this. """


def parse(src, pattern=PATTERN):
    """ Converts plain-text input into computer-friendly form. """
    for line in src.splitlines():
        line = line.strip()  # remove meaningless white-spaces, just best practices
        if not line or line.isspace():  # line.isspace() is redundand on stripped lines
            continue  # ignore empty lines
        # we do not compile the regexp because it is automatically compiled and
        # cached inside re module
        match = re.search(pattern, line)  # or re.match if lines are stripped
        if not match:
            raise ParseError("failed to parse: %s" % line)
        # actually we don't know the currency, but let's think it is dollars
        rawcount, descr, price = match.groups()
        yield (int(rawcount), descr, Decimal(price))


def what_taxes(descr):
    """ Extract tax information from description.
        Returns tuple of what taxes to be paid.
    """
    sales_tax = True
    import_tax = False
    descr = descr.lower()  # for case insensitive matching

    if descr.find("imported") != -1:
        import_tax = True

    for marker in TAX_EXEMPT_MARKERS:
        if descr.find(marker) != -1:
            sales_tax = False
            break

    return sales_tax, import_tax


def round005(x):
  """ Rounds towards nearest 0.05. """
  return Decimal(round(x/Decimal("0.05")))*Decimal("0.05")


def tax_round005(price, amount):
    """ Apply taxes with rounding towards nearest 0.05. """
    tax = round005(price * amount)
    return tax


def process_input(data, stream=stdout):
    sales_taxes = Decimal("0.00")
    total = Decimal("0.00")
    for count, descr, price in parse(data):
        subtotal = Decimal("0.00")
        for i in range(count):
            apply_sales_tax, apply_import_duty = what_taxes(descr)
            subtotal += price
            if apply_sales_tax:
                sales_tax = tax_round005(price, SALES_TAX)
                sales_taxes += sales_tax
                subtotal += sales_tax
            if apply_import_duty:
                import_duty = tax_round005(price, IMPORT_DUTY)
                subtotal += import_duty
                sales_taxes += import_duty
            total += subtotal
        print(OUTPUT_FMT.format(count=count,
                                descr=descr, price=subtotal), file=stream)
    print("Sales Taxes:", sales_taxes, file=stream)
    print("Total:", total, file=stream)


if __name__ == '__main__':
    print("Program for calculating taxes.")
    print("Reading from stdin (Ctrl+D to finish)")
    process_input(stdin.read())
