This is the 2nd version of 100 female celebrities data.

- Raw >> P1: extract.py, extract all related info

- P1 >> P2: formulate.py, build the input structure for the REASTAP implementation

- P2 >> P3: convert.py, determine the  "column_types","key_column","numeric_columns"and "date_columns" based on the table info (regex) … should rather use DAGOBAH!

***

- Raw >> P4: supply.py, determine the  "column_types","key_column" using DAGOBAH

- P4 >> P5: rct.py, refine the column type.

- P5 >> P6: date.py, use 9999 as placeholder for empty date vlue in date_column.



