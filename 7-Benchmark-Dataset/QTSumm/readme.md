# QTSumm Dataset Recovery

This directory contains the workflow and results for recovering the QTSumm dataset using a combination of Google Search and Wiki-API methods.

## Directory Structure

- **`original-json`**: Contains the original QTSumm JSON files.
- **`google`**: Contains the code and results from the Google Search approach.
- **`wiki-api`**: Contains the code and results from the Wiki-API search.
- **`combined`**: Contains the combined results from both the Google and Wiki-API approaches.
- **`recovery`**: Contains the final recovery results.
- **`stats`**: Contains statistical analysis of the original QTSumm dataset.

## Recovery Workflow

### 1. URL Recovery Based on Wiki-page Title

#### a. Google Search
- Perform a Google search using the format: `wiki-page title + site:wikipedia.org`.
- Select the top 3 results and form corresponding Wikipedia URLs.
- Match the titles and calculate the title similarity.
- Generate a `.csv` file for each JSON file containing the results.

#### b. Wiki-API
- Use the Wiki-API to search for the wiki-page title.
- Select the top 3 results and form corresponding Wikipedia URLs.
- Match the titles and calculate the title similarity.
- If the table is a disambiguation page, scan all possible URLs and select the one with the highest table similarity score.
- Generate a `.csv` file for each JSON file containing the results.

### 2. Table Selection Based on Similarity Comparison
- For each URL candidate, scan all tables on the wiki-page.
- Convert each table (4 rows + 1 header, first 4 columns) into strings.
- Calculate the table similarity score.
- Select the table with the highest similarity score.

### 3. Combine Both Approaches
- Calculate the overall similarity using the formula: `int(0.4 * row['title_similarity'] + 0.6 * row['table_similarity'])`.
- Select the table with the highest overall similarity score between both approaches.

