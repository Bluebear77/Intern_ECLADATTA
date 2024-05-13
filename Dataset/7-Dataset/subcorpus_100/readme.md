Here is the subcorpus for the ECLADATTA project.

It has 3 corpora: Business, Telco and Celebrity. Each with 100 examples.

*_stats.json: contains the statistics of the JSON file.
```
{
    "nb_tables": [total_number_of_tables],
    "nb_pages": [total_number_of_pages],
    "nb_pages_with_table": [number_of_pages_with_tables],
    "avg_text_size_per_page": [average_text_size_per_page],
    "max_text_size_per_page": [maximum_text_size_per_page],
    "min_text_size_per_page": [minimum_text_size_per_page],
    "avg_paragraphs_per_page": [average_paragraphs_per_page],
    "max_paragraphs_per_page": [maximum_paragraphs_per_page],
    "min_paragraphs_per_page": [minimum_paragraphs_per_page],
    "avg_tables_per_page": [average_tables_per_page],
    "max_tables_per_page": [maximum_tables_per_page],
    "min_tables_per_page": [minimum_tables_per_page],
    "avg_rows_per_tables": [average_rows_per_table],
    "max_rows_per_tables": [maximum_rows_per_table],
    "min_rows_per_tables": [minimum_rows_per_table],
    "avg_columns_per_tables": [average_columns_per_table],
    "max_columns_per_tables": [maximum_columns_per_table],
    "min_columns_per_tables": [minimum_columns_per_table],
    "avg_cells_per_tables": [average_cells_per_table],
    "max_cells_per_tables": [maximum_cells_per_table],
    "min_cells_per_tables": [minimum_cells_per_table]
}

```

*_cat.json:

```
{
  "_index": "[index_name]",
  "_id": "[entity_name]",
  "_source": {
    "name": "[entity_name]",
    "nbPages": [number_of_pages],
    "children": ["[list_of_associated_entities]"],
    "updatedDate": "[last_updated_date]"
  }
}

```

