import csv
import json
import random
import re
from datetime import datetime
from os.path import join

from Exam import Exam
from Question import Question


def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def validate_date(date_str):
    if date_str is None:
        return True
    return re.match(r'^\d{6}$', date_str) is not None

class ExamManager:
    def __init__(self, database_folder_path):
        """
        Initialize the ExamManager with the path to the exam database folder.
        The folder should contain the following files:
        - Questions.csv
        - Points.json
        - Requirements.json
        """
        self.questions_file = join(database_folder_path, "Questions.csv")
        self.points_file = join(database_folder_path, "Points.json")
        self.requirements_file = join(database_folder_path, "Requirements.json")
        self.questions = self.load_questions(self.questions_file)
        self.points = load_json(self.points_file)
        self.requirements = load_json(self.requirements_file)

    def load_questions(self, file):
        questions = []
        with open(file, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                last = row.get("last", None)
                if last:
                    if not validate_date(last):
                        raise ValueError(f"Invalid date format for 'last': {last}")
                else:
                    last = datetime.now().strftime(r'%y%m%d')
                questions.append(Question(
                    type=row["type"],
                    topic=row["topic"],
                    title=row["title"],
                    wording=row["wording"],
                    choices=row["choices"],
                    solution=row["solution"],
                    explanation=row["explanation"],
                    status=row["status"],
                    counter=int(row.get("counter", 0)),
                    last=last
                ))
        return questions

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
            self.confirm_exam(exam)
            print("Exam confirmed and usage data updated.")
            print("Exam blueprint and questions exported.")
        else:
            print("Exam not confirmed. Nothing happens.")

    def confirm_exam(self, exam):
        exam.to_markdown()
        exam.to_csv()
        exam.to_pdf()
        for question in exam.questions:
            question.increment_counter()
        self.save_questions()

    def save_questions(self):
        with open(self.questions_file, 'w', newline='') as f:
            fieldnames = ["type", "topic", "title", "wording", "choices", "solution", "explanation", "status", "counter", "last"]
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for question in self.questions:
                writer.writerow(question.to_dict())

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

if __name__ == "__main__":
    manager = ExamManager(".")
    exam = manager.create_exam("AE2230-I_Resit2_241204")
    manager.review_exam(exam)