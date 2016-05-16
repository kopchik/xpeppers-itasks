#!/usr/bin/env python3

"""
Calculates sales taxes. Please see README for description.
"""

import re       # regexp routines
from decimal import Decimal, ROUND_HALF_EVEN  # fixed point arithmetics


TAX_EXEMPT_MARKERS = "book chocolate food pills".split()
PATTERN = r"([0-9]+) (.+) at ([0-9]+\.[0-9]+)"
SALES_TAX = Decimal("0.10")    # 10% sales tax
IMPORT_DUTY = Decimal("0.05")  # 5% import duty
OUTPUT_FMT = "{count} {descr}: {price}"


def what_taxes(descr):
  """ Extract tax information from description.
      Returns tuple of what taxes to be paid.
  """
  sales_tax  = True
  import_tax = False
  descr = descr.lower() # for case insensitive matching

  if descr.find("imported") != -1:
    import_tax = True

  for marker in TAX_EXEMPT_MARKERS:
    if descr.find(marker) != -1:
      sales_tax = False
      break

  return sales_tax, import_tax


def tax_round005(price, amount):
  tax = price * amount
  # round towards nearest 0.05
  tax = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
  return tax



# TODO: error handling
def parse(src, pattern=PATTERN):
  result = []
  errors = []
  for line in src.splitlines():
    line = line.strip()
    if not line:
      continue  # ignore empty lines
    # we do not compile the regexp because it is automatically compiled and cached inside re module
    match = re.match(pattern, line)
    if not match:
      errors.append("failed to parse: %s" % line)
      continue
    # actually we don't know the currency, but let's think it is dollars
    count, descr, price = match.groups()
    count = int(count)
    yield (count, descr, Decimal(price))


def apply_taxes(price, exempt, imported):
  newprice = price
  if not exempt:
    newprice = tax_round005(price, SALES_TAX)
  if imported:
    amount *= Decimal("1.05")
    amount = myround(amount)


def main(data):
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
         subtotal += tax_round005(price, SALES_TAX)
      total += subtotal
    print(OUTPUT_FMT.format(count=count, descr=descr, price=subtotal))
  print("Sales Taxes:", sales_taxes)
  print("Total:", total)


if __name__ == '__main__':
  data= """
2 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85
"""
  main(data)

