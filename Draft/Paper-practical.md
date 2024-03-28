## "Turning Tables: Generating Examples from Semi-structured Tables for Endowing Language Models with Reasoning Skills"
Github:https://github.com/oriyor/turning_tables/blob/main/ExampleGeneration/ExampleGeneration/common/question_template_utils.py


## ExampleGeneration/ExampleGeneration/common/question_template_utils.py:

process question templates by substituting any named templates that are referenced within the list.

- `substitute_named_templates`: updates templates by filling in placeholders with details from a predefined set of templates (named_templates). 

- `process_question_templates` starts with a list of templates, where the first item should be a dictionary called NamedTemplates, containing predefined templates. It uses these named templates to enrich the rest of the templates in the list by replacing their copy_from references with the actual content from NamedTemplates.


## ExampleGeneration/ExampleGeneration/common/questions_utils.py:
Sampling and combining questions in a question-answering dataset, facilitate the creation of diverse and complex question sets from simpler components.

- `sample_questions_per_template(questions, sample_size)`:

  Purpose: Samples a specified number of questions (sample_size) for each question template variation found in a list of questions.<br/>
  Example: If there are 50 questions with 5 different templates and sample_size=5, this function returns up to 25 questions, ensuring 5 questions per template are sampled.

- `sample_questions(questions, sample_size)`:

  Purpose: Randomly samples a given number of questions (sample_size) from a list.<br/>
  Example: From a list of 100 questions, if sample_size=10, it returns a random subset of 10 questions.

- `get_composite_question(first_comp_question, second_comp_question)`:

  Purpose: Combines two questions into a composite question by injecting the answer of the first into the text of the second.<br/>
  Example: Combining "What is the capital of France?" (Answer: Paris) with "Which city hosts the Eiffel Tower?" results in "Which city hosts the Eiffel Tower? (What is the capital of France? : Paris)".

- `get_conjunction_question(q1, q2, intersecting_answers)`:

  Purpose: Creates a conjunction question by combining two questions with 'and', focusing on their intersecting answers.<br/>
  Example: Joining "What are EU countries?" and "Which countries use the euro?" might result in "What are EU countries and which countries use the euro?" if the intersecting answers are countries in the EU that use the euro.

  ## ExampleGeneration/ExampleGeneration/configurations/config_reas.json:
- `GenQuestionsFromTemplates_TabReas`: Generates synthetic questions from predefined templates, targeting a range of question types like comparisons, superlatives, arithmetic, and more. It's set to create up to 10 million examples using 20 processes, taking "ClassifyTableColumnsFiltered.jsonl" as input and outputting to "PseudoLangQuestions_All.jsonl".
  
- `FormatSyntheticQuestions`: Formats the generated questions into triplets of `question, context, and answer`. This stage is limited to formatting 100,000 examples with a single process and outputs to "FormattedQuestions.jsonl".


## ExampleGeneration/ExampleGeneration/datajobs/format_questions.py:

  Input: Raw question data about a Wikipedia page's table. <br/>
  Operation: The class takes this data and, for a given question, constructs a context string that includes the table and page title. It then combines this with the question and its answers, shuffling associated facts and distractors for variety.
  Output: A structured object that looks like this:
  ```
  {
    "qid": "Q123",
    "question": "What is the capital of France?",
    "context": "In the List of Countries and Capitals of Europe: France is known for its rich history and culture.",
    "answer": "Paris",
    "url": "https://en.wikipedia.org/wiki/France",
    "page_title": "France",
    "table_title": "Countries and Capitals"
  }
  
  ```

## ExampleGeneration/ExampleGeneration/question_templates/tabreas_question_templates.json:


https://github.com/oriyor/turning_tables/blob/main/ExampleGeneration/ExampleGeneration/question_templates/tabreas_question_templates.json


