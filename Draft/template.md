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
