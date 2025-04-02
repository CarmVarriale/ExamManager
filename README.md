# ExamManager

The `ExamManager` repository is designed to create and manage exams consisting (for now) of true/false, multiple choice, and numerical questions. 
It provides functionalities to load question banks from a CSV file, create exams based on specific requirements when it comes to questions per topic, and export the exam blueprint in various formats (Markdown, CSV, and PDF).

## Structure

- **ExamManager.py**: Contains the `ExamManager` class, which handles loading question banks, creating exam instances, reviewing questions, replacing questions, and approving exams. It also includes an example of use.
- **Exam.py**: Contains the `Exam` class, which represents an exam and provides low-level methods to add, replace, and export questions.
- **Question.py**: Contains the `Question` class, which represents a question and provides methods to increment use count, update the last date it was used, and convert to dictionary format.
- **Questions.ssv**: A semicolon separated CSV file collecting questions and their relevant data categorized by type.
- **Points.json**: A JSON file indicating the points assigned to each type of question.
- **Structure.json**: A JSON file indicating the number of question and question types per topic to be used to assemble a given exam.

## Usage
  
```python
manager = ExamManager("path/to/database/folder")
```
The database folder should contain the following files: `Questions.ssv`, `Points.json`, `Structure.json`

```python
exam = manager.create_exam("ExamName/Type/Date")
manager.review_exam(exam)
```
The `review_exam` method starts an interactive review session with the user.

## Managing the Question Bank
You can view and manipulate the `Questions.ssv` file by opening it in VSCode using the [Rainbow CSV](https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv) and the [Edit CSV](https://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv) extensions. 

Please refrain to use Microsoft Excel, as it is not able to preserve the correct format of the document.

## Export Formats

- **Markdown**: The exam blueprint is exported to a Markdown file.
- **CSV**: The exam blueprint is exported to a CSV file.
- **PDF**: The exam blueprint is exported to a PDF file.

## TODO

- [x] Provide a comprehensive example of database files, with at least three questions per type per topic
- [x] Simplify and coordinate topic labels
- [ ] Modify ExamManager to allow selecting a databases, points and structure files  
- [ ] Store a way to understand the solution procedure in one string (example: correct choice, python code for numerical calculation, reasoning for true/false)
- [ ] Create a grading grid to assign different points to different types of numerical questions. For example: straightforward solution process should be worth less than inverse solution process, or one that requires a more complex derivations where certain things simplify.