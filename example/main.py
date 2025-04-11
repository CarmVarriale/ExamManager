# Import the ExamManager class from the ExamManager module
import pathlib, sys
_parentdir = pathlib.Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(_parentdir))

from ExamManager import ExamManager

manager = ExamManager(
    "questions_example.ssv",
    "points_example.json", 
    "structure_example.json")

exam = manager.create_exam("GenKnowledge_ExamExample_250414")

# start an interactive review and approval session, ending with export
manager.review_exam(exam) 

# OR

# directly export the exam to various formats
# exam.export_to_csv() 
# exam.export_blueprint_to_markdown()
# exam.export_blueprint_to_pdf()
