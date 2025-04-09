# ExamManager

This simple package provides simple functionalities to manage exam creation, review and monitoring through time.
In a nuthsell:
- create exams on the basis of a question bank, an exam structure file, and a points file
- review the questions selected for the exam, and approve the exam before it is given to the students
- keep track of the questions that have been used in the past, and their last date of use
- export the exam blueprint in various formats (Markdown, CSV, and PDF)

For the exam creation, a simple algorithm selects questions from the question bank on the basis of the provided exam structure, the amount of times a question has appeared before, the last time it has appeared, and a random seed.
Question variants that assess the same skill or learning objective are prevented to appear in the exam.

## Structure
- ``ExamManager.py``: Implements the `ExamManager` class, responsible for managing the exam lifecycle, including loading question banks, creating exams, reviewing and replacing questions, and approving exams. It also includes usage examples.
- ``Exam.py``: Defines the `Exam` class, which encapsulates an exam's structure and provides low-level methods for adding, replacing, and exporting questions.
- ``Questions.ssv``: A semicolon-separated file containing the question bank with all relevant question metadata, including a counter of how many times a question has been used and the last time it has been used in an approved exam.
- ``Points.json``: A JSON file specifying the points assigned to each question type and topic, and defaults points per type.
- ``Structure.json``: A JSON file defining the exam structure in terms of order of topics, and number and types of questions per topic.

## Usage

See the `main.py` file for an executable example of how to use the `ExamManager` class

1. Create an exam manager instance which can create and manage exams on the basis of a selected question bank, points file and structure file:
    ```python
    from ExamManager import ExamManager

    manager = ExamManager(
        "QuestionsExample.ssv",
        "PointsExample.json", 
        "StructureExample.json") 
    ```

1. Create the instance of an exam and give it a representative name:
    ```python
    exam = manager.create_exam("AE2230-I_Resit2_241204")
    ```

1. Start an interactive session to review the questions selected for the exam, replace some of them if needed, and eventually approve and export the exam:
    ```python
    exam.review_questions()
    ```

## Installation

1. Install [Python 3.12 or higher](https://www.python.org/downloads/) and optionally add it to your PATH.
2. Clone the repository from Github: 

    ```git clone https://github.com/CarmVarriale/ExamManager```

3. Navigate to the cloned directory:

    ```cd your/path/to/ExamManager```

4. Create a virtual environment (optional but recommended):

    ```python -m venv .venv```

5. Activate the virtual environment:
   - On Windows: ```.\.venv\Scripts\activate```
   - On macOS/Linux: ```source .venv/bin/activate```

6. Install the required dependencies:
   - On Windows: ```pip install -r requirements.txt```
   - On macOS/Linux: ```pip install -r requirements.txt```

## Managing the Question Bank
You can view and manipulate the `Questions.ssv` file by opening it in the [VSCode](https://code.visualstudio.com/) editor using the [Rainbow CSV](https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv) and the [Edit CSV](https://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv) extensions. 

Please DO NOT to use Microsoft Excel, as it is not able to preserve the correct format of the document.

## Export Formats

The exam blueprint is exported to a CSV file, a Markdown file and a PDF file.
You will have to manually define the exam in a virtual environment such as Mobius or Ans.

## Contribution
Contributions are welcome and encouraged through Issues and Pull Requests.
For major changes, please open an issue first to discuss what you would like to change.

## Contributors

