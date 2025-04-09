from ExamManager import ExamManager

manager = ExamManager(
    "QuestionsExample.ssv",
    "PointsExample.json", 
    "StructureExample.json") 
exam = manager.create_exam("GenKnowledge_ExamExample_250414")
manager.review_exam(exam)