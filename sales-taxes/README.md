# Sales Taxes Problem

In two words: calculate taxes and total price for a list of items (see https://github.com/xpeppers/sales-taxes-problem for details).

## General Architecture
Written in functional style.
The idea is to split the program into small units easy to test.
There is one main function ("process_input") that glues all them together and produces the output.

I used fixed-point arithmetics for storing and processing money values.
Floating-point operations are no good for money [1].
It is possible to use libraries especially designed for this, but I think for an interview
task it's better to stick with built-in data structures.
The handling of money operations follows best practices [2].
The code is checked with a static code checker (``pyflakes3``) and formatting checker (``autopep8``).

I decided not to add a configuration layer because it feels like an over-engineering for this task.

## Tests

The program id accompanied wnit-tests and a few "full-stack" ~~integration~~ validation tests to ensure the final result.
Just run ``py.test -sv`` in the program's folder.
Tests are known to fail, please see "Other" section for info.
The coverage is not 100% (particulary, functions not tested for invalid input), but... I'm on vacation, sorry :).


## Performance analysis

At first glance there are no obious performance bottlenecks at first glance.
Regexps are cached internally.

## Error handling

It uses "let it fail" and "all or nothing" error handling approaches: an error in computation will terminate the program with no results, but with error message.

## Other

It was not mentioned explicitly in the task, but I infered that the first field (column) in the input is the number of items.
This is taken into account.

The format provided for input does not allow for precise detection of goods exempt from sales taxes. I used simple keyword matching to detect "books, food, and medical products that are exempt".

I'm not sure provided tests are 100% correct. There are two concerns:

1. In test 3 in output "1 box of imported chocolates at 11.25" the word "imported" does not match the position in the input "1 imported box of chocolates: 11.85".

2. The way rounding is applied remains obscured to me. For "1 box of imported chocolates at 11.25" the provided output does not match manual calculation:
~~~
11.25 + round(11.25*0.05) = 11.25 + round(0.5625) = 11.25 + 0.6 = 11.80
~~~
So we got 11.80 here, while in the provided output it is 11.85 which looks incorrect to me.

## References

[1] http://stackoverflow.com/questions/3730019/why-not-use-double-or-float-to-represent-currency  
[2] http://www.yacoset.com/how-to-handle-currency-conversions
