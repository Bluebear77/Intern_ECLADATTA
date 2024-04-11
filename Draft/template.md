## Reasoning

| Reasoning | Example of Fact Templates | Example of Fact |
|-----------|---------------------------|-----------------|
| Conjunction | The `col1` that have `CONDITION` are `executed_results`. | The Player Name that have Country is Canada are Corey Conners, Nick Taylor, Adam Svensson. |
| Counting | `executed_results col:1` have `col:2 CONDITION:2`. | 2 Game have Attendance greater than 10,235. |
| Temporal or Numerical Order | The `col:1` ordered by `col:3` are `executed_results`. | The Company ordered by Sales are Apple, Nvidia, Google, (...abbreviate...) |
|  | The `col:1`, with `col:2 CONDITION:2`, ordered by `col:3` are `executed_results`. | The institutions that Founded year is earlier than 1860 are Adrian College, Michigan State University. |
| Temporal or Numerical Comparison | The `col:1` that `col:2 CONDITION:2` are `executed_results`. | The sum of Earning with Point is greater than 140 is 430,027. |
| Numerical Operation (Sum, Avg) | The `OPERATOR` of `col:1` with `col:2 CONDITION:2` is `executed_results`. |  |
| Numerical Operation (Diff) | The difference between `val:1` and `val:2` in `col` is `executed_results`. | The difference between China and Canada in Gold is 16. |

**Table 7**: 6 reasoning operations, along with fact template and examples, defined for the fact generation process of REFACToR. Variable names indicate permissible instantiations. `col` denotes a column name, `val` denotes a cell value, and `executed_results` denotes the execution results of the function. `OPERATOR` is instantiated according to the specific reasoning operation, e.g., for "Numerical Operation", `OPERATOR` is replaced with "sum" or "average"; `CONDITION` can be 1) a cell value from the i-th column, or 2) number/temporal comparison statement (e.g. "later than 1967") if the i-th column is of number or date type.

***



| Reasoning | Example Templates | Example Questions & Answers | % Data |
|-----------|-------------------|-----------------------------|--------|
| Conjunction | What was the `col:1` when the `col:2` was `CONDITION:2` and the `col:3` was `CONDITION:3`? | Q: What was the Television Service when the Country was Italy and the Content was Sport? <br> A: Sky OMC Sports, ESPN, Gazzetta TV, ... <br> 21.6% |
| Quantifiers Only/Every | Does `OPERATOR` `col:1`, with `col:2` was `CONDITION:2`, have `col:3` `CONDITION:3`? | Q: Does every Company, with Headquarter was Paris, have Industry Financials? <br> A: Yes <br> Q: Does only Company Name, with Founded Year was later than 1964, have Employee Number greater than 30,000? <br> A: No <br> 10.3% |
| Temporal Comparison | Which `col:1`, with `col:2` was `CONDITION:2`, happened the `ORDINAL` according to `col:3`? | Q: Which Romaji, with Sales was greater than 203,471, happened the 4th according to Date? <br> A: Hepburn <br> 14.5% |
| Date Difference | how much time had passed between when the `col:1` was `val:1` and when the `col:2` was `val:2`? | Q: how much time had passed between when the Candidate was John Kufuor and when the Candidate was Paul McCartney? <br> A: 16 years <br> 5.7% |
| Counting | How many `col:1` have `col:2` `CONDITION:2`? | Q: How many Event Location have Attendance greater than 10,235? <br> A: 7 <br> 18.0% |
| Numerical Operation | What was the `OPERATOR` of `col:1` when the `col:2` was `CONDITION:2`? | Q: What was the sum of GDP Estimate (US Million) when the GDP Estimate (US Million) was greater than 841,969? <br> A: 1,574,013 <br> 15.9% |
| Numerical Comparison | Which `col:1`, with `col:2` was `CONDITION:2`, has the `ORDINAL` `col:3` `CONDITION:3`? | Q: Which Franchise, with Owner(s) was Nintendo, has the 5th Total revenue($ US Billion)? <br> A: Pokemon <br> 14.0% |

#### Table 1: Reasoning skills with example for pre-training REAsTAP
Variable names indicate permissible instantiations. `col` denotes a column name, `val` denotes a cell value, and indices denote that a cell value must originate from the specified column. `OPERATOR` and `ORDINAL` correspond to operations and ordinal numeral that are instantiated according to the specific reasoning skill, e.g., for “Temporal Comparison”, `ORDINAL` is replaced with a reasonable ordinal numeral such as “4th”. And `CONDITION :i` can be 1) a cell value from the i-th column, or 2) number/temporal comparison statement (e.g. "later than 1967") if the i-th column is of number or date type.
