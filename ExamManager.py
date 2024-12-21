import json
import random
import pandas as pd
from datetime import datetime
from os.path import join

from Exam import Exam
from Question import Question


def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

class ExamManager:
    def __init__(self, database_folder_path):
        """
        Initialize the ExamManager with the path to the exam database folder.
        The folder should contain the following files:
        - Questions.ssv
        - Points.json
        - Requirements.json
        """
        self.questions_file = join(database_folder_path, "Questions.ssv")
        self.points_file = join(database_folder_path, "Points.json")
        self.requirements_file = join(database_folder_path, "Requirements.json")
        self.questions = self.load_questions(self.questions_file)
        self.points = load_json(self.points_file)
        self.requirements = load_json(self.requirements_file)

    def load_questions(self, file):
        df = pd.read_csv(file, delimiter=';', dtype=str)
        questions = []
        for _, row in df.iterrows():
            last = row["last"]
            if pd.isna(last):
                last = datetime.now().strftime(r'%y%m%d')
            else:
                last = datetime.strptime(last, r'%y%m%d').strftime(r'%y%m%d')
            questions.append(Question(
                type=row["type"],
                topic=row["topic"],
                title=row["title"],
                wording=row["wording"],
                choices=row["choices"],
                solution=row["solution"],
                explanation=row["explanation"],
                status=row["status"],
                counter=int(row["counter"]),
                last=last
            ))
        return questions
    
    def sort_questions(self, *args):
        VALID_HEADERS = ["type", "topic", "title", "wording", "choices", "solution", "explanation", "status", "counter", "last"]
        for arg in args:
            if arg not in VALID_HEADERS:
                raise ValueError(f"Invalid header '{arg}'. Valid headers are: {', '.join(VALID_HEADERS)}")
        df = pd.read_csv(self.questions_file, delimiter=';', dtype=str)
        df = df.sort_values(by=list(args))
        df.to_csv(self.questions_file, sep=';', index=False)

    def save_questions(self):
        df = pd.DataFrame([q.to_dict() for q in self.questions])
        df.to_csv(self.questions_file, sep=';', index=False)

    def replace_question(self, exam, index_to_replace):
        question_to_replace = exam.questions[index_to_replace - 1]
        question_pool = [
            q for q in self.questions
            if q not in exam.questions 
            and q != question_to_replace 
            and q.type == question_to_replace.type 
            and q.topic == question_to_replace.topic
        ]
        if not question_pool:
            print(f"No replacement question available for "
                  f"type '{question_to_replace.type}' and "
                  f"topic '{question_to_replace.topic}'.")
            return False
        replacement_question = random.choice(question_pool)
        exam.replace_question(index_to_replace - 1, replacement_question)
        return True

    def create_exam(self, exam_name):
        exam = Exam(exam_name)
        for topic, types in self.requirements.items():
            for type, count in types.items():
                question_pool = sorted(
                    [q for q in self.questions 
                     if q.type == type 
                     and q.topic == topic],
                    key=lambda q: q.counter
                )
                if len(question_pool) < count:
                    raise ValueError(
                        "Not enough questions of type '{}' "
                        "for topic '{}' available.".format(type, topic))

                selected_questions = question_pool[:count]
                for question in selected_questions:
                    question.points = self.points[type].get(
                        topic, 
                        self.points[type].get("default", 1))
                    exam.add_question(question)
        return exam

    def review_exam(self, exam):
        # Ask if the user wants to replace a question repeatedly until no
        while True:
            exam.print_blueprint()
            index_to_replace = int(
                input(
                    "\nWould you like to replace a question?"
                    "\n- If yes, enter its index number"
                    "\n- If no, enter 0\n"))
            if index_to_replace == 0:
                break
            if self.replace_question(exam, index_to_replace):
                print("Updated exam questions.")
                
        # Ask to confirm the exam after user approval
        user_input = input(
            "\nDo you approve the exam?"
            "\n- If 'yes', question counters and dates are going to be updated,"
            " and the blueprint is going to be exported."
            "\n- If 'no', nothing happens\n").strip().lower()
        if user_input == "yes":
            self.approve_exam(exam)
            print("Exam approved and usage data updated.")
            print("Exam blueprint and questions exported.")
        else:
            print("Exam not confirmed. Nothing happens.")

    def approve_exam(self, exam):
        exam.to_markdown()
        exam.to_csv()
        exam.to_pdf()
        for question in exam.questions:
            question.increment_counter()
        self.save_questions()

if __name__ == "__main__":
    manager = ExamManager(".")
    manager.sort_questions("type", "topic", "title")
    exam = manager.create_exam("AE2230-I_Resit2_241204")
    manager.review_exam(exam)