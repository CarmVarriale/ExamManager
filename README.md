# ExamManager

The `ExamManager` repository is designed to create and manage exams consisting (for now) of true/false, multiple choice, and numerical questions. 
It provides functionalities to load question banks from a CSV file, create exams based on specific requirements when it comes to questions per topic, and export the exam blueprint in various formats (Markdown, CSV, and PDF).

## Structure

- **ExamManager.py**: Contains the `ExamManager` class, which handles loading question banks, creating exam instances, reviewing questions, replacing questions, and approving exams. It also includes an example of use.
- **Exam.py**: Contains the `Exam` class, which represents an exam and provides low-level methods to add, replace, and export questions.
- **Question.py**: Contains the `Question` class, which represents a question and provides methods to increment use count, update the last date it was used, and convert to dictionary format.
- **Questions.csv**: A CSV file containing an example database of questions categorized by type.
- **Points.json**: A JSON file containing an example for the points assigned to each type of question.
- **Requirements.json**: A JSON file containing an example of requirements for creating an exam.

## Usage
  
```python
manager = ExamManager("path/to/database/folder")
```
The database folder should contain the following files: `Questions.csv`, `Points.json`, `Requirements.json`

```python
exam = manager.create_exam("ExamName/Type/Date")
manager.review_exam(exam)
```
The `review_exam` method starts an interactive review session with the user.

## Export Formats

- **Markdown**: The exam blueprint is exported to a Markdown file.
- **CSV**: The exam blueprint is exported to a CSV file.
- **PDF**: The exam blueprint is exported to a PDF file.

## TODO

- [x] Provide a comprehensive example of database files, with at least three questions per type per topic
- [ ] Find a way to store the Python solution code for numerical questions
- [ ] Include solutions in the CSV database for all question types
- [ ] Include explanations in the CSV database for all question types
- [ ] Print solutions in the blueprint