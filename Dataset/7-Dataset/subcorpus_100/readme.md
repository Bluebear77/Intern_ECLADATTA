Here is the subcorpus for the ECLADATTA project.

It has 3 corpora: Business, Telco and Celebrity. Each with 100 examples.


- *_doc.json: contains detailed info of each instance.

```
{
  "_index": "[index_name]",
  "_id": "[document_id]",
  "_source": {
    "identificationMetadata": {
      "id": "[document_id]",
      "title": "[document_title]",
      "url": ["[url_list]"],
      "version": [version_number],
      "versionDate": "[version_date]",
      "hash": "[hash_value]",
      "wikidata": "[wikidata_id]"
    },
    "descriptionMetadata": {
      "categories": ["[list_of_categories]"],
      "language": "[language]",
      "source": "[source]"
    },
    "contentMetadata": {
      "format": "[content_format]",
      "content": "[content_text]"
    },
    "collectMetadata": {
      "requestedDate": "[request_date]",
      "ingestedDate": "[ingest_date]"
    },
    "extractionMetadata": [{
      "id": "[extractor_id]",
      "linkExtractionDate": "[link_extraction_date]",
      "links": [{
        "fragment": "[fragment]",
        "link": "[link]",
        "text": "[link_text]",
        "title": "[link_title]"
      }],
      "nbLinks": [number_of_links],
      "nbTables": [number_of_tables],
      "nbTexts": [number_of_texts],
      "tableExtractionDate": "[table_extraction_date]",
      "tables": [],
      "technology": "[extraction_technology]",
      "textExtractionDate": "[text_extraction_date]",
      "texts": [{
        "endOffset": [end_offset],
        "index": [text_index],
        "level": [text_level],
        "startOffset": [start_offset],
        "title": "[text_title]",
        "value": "[text_value]"
      }]
    }],
    "statsMetadata": {
      "textSize": [total_text_size]
    }
  }
}

```

- *_stats.json: contains the statistics of the JSON file.
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

- *_cat.json:contains the key index info of each instance.

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

