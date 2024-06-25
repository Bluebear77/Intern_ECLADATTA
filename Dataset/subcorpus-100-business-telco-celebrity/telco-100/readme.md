Here is the working stream of the 100 telco instances.

Complete: pages with all tables extracted

Missing: pages that have tables in the origin URL but none were extracted. Some are due to unparsed templates, others are just ordinary "wikitable sortable".

NoTable: pages that have no tables in the URL

Raw: the original *_doc.json splited per URL.

***

- Complete >> P1: extract.py, extract all related info

- P1 >> P2: formulate.py, build the input structure for the REASTAP implementation

- P2 >> P3: supply.py, determine the  "column_types","key_column" using DAGOBAH