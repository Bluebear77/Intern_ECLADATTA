# ECLADATTA CorpusWalker Quick Start Guide

## Accessing the Console UI
No personal authentication is needed. Login as ECLADATTA to access the console UI.
- Console UI: [https://corpuswalker.ecladatta.eurecom.fr/console](https://corpuswalker.ecladatta.eurecom.fr/console)

## Using the Platform
- **Listing Corpus & Searching Documents**: Utilize the UI to list corpus or search documents.
- **Subcorpus Information**: The subcorpus `personnalitesfeminines_fr` contains 252,938 Wikipedia pages in French.

## Exporting Documents
- **UI Export Limit**: Export directly from the UI is limited to 10,000 documents (synchronous request).
- **Full Dump via API**:

  - **The API Documentation:** [https://corpuswalker.ecladatta.eurecom.fr/swagger](https://corpuswalker.ecladatta.eurecom.fr/swagger)
  - Start dump: `/api/v1/doc/dump/{corpus_id}/trigger` - Launches execution in a worker, returns a `task_id`.
  - Check progress: `/api/v1/doc/dump/{task_id}/status` - To see the export task progress.
  - Retrieve dump: `/api/v1/doc/dump/{task_id}/result` - To get the dump when the export task is complete.
- **Scroll Option**: Use `/api/v1/doc/search` or `/api/v1/doc/export` with the scroll option for filters.


***
# Problems:

## Multiple instances in `personnalitesfeminines_fr` is male.

For example:
`Chawki Bentayeb`in is actually a male.

![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/0b1a0e1d-049b-4b27-a718-62d0d1967630)
![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/1508f108-4966-462e-93d7-6a6fc1003773)

Also:
```
Salaheddine Benhamadi
Mario David
Akio Ōtsuka
Mattia Viel
Gonzalo Andrés
Andries Malan
```
