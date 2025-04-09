import json
import pandas as pd
from datetime import datetime

from Exam import Exam, QUESTION_PARAMS

class ExamManager:
    """Class to create and manage the exams"""
    def __init__(self, questions_file, points_file, structure_file):
        self.qfile = questions_file 
        self.points = json.load(open(points_file, 'r'))
        self.structure = json.load(open(structure_file, 'r'))
        self.qbank = self.parse_questionbank_from_file(self.qfile)

    def parse_questionbank_from_file(self, question_file):
        """Parse the question bank from a .ssv file and add points to each question based on its type and topic. The points are read from a json file."""
        qbank = pd.read_csv(question_file, delimiter=';', dtype=str)
        qbank["points"] = qbank.apply(
            lambda q: 
                self.points[q["type"]].get(
                    q["topic"], 
                    self.points[q["type"]].get("default", None)
            ), 
            axis=1
        )
        return qbank
        
    def sort_questionbank_by(self, *args):
        """Sort the question bank by the given parameters. The parameters must be valid headers in the question bank."""
        for arg in args:
            if arg not in QUESTION_PARAMS:
                raise ValueError(f"Invalid param '{arg}'. Valid headers are: {', '.join(QUESTION_PARAMS)}")
        self.qbank = self.qbank.sort_values(by=list(args))
        
    def save_questionbank_to_file(self):
        """Save the question bank to a .ssv file. The points column is dropped before saving as it depends on the provided points file, which may change for different exams."""
        self.qbank.drop(columns=["points"], inplace=True)
        self.sort_questionbank_by("topic","type","title", "variant", "counter", "last_used")
        self.qbank.to_csv(self.qfile, sep=';', index=False)

    def create_exam(self, exam_name):
        """Create an exam based on the provided structure. The structure is a dictionary where the keys are topics and the values are dictionaries with question types as keys and the number of questions as values.
        
        Exam questions are selected randomly from the question bank, under the constraints of the structure. The questions are sorted by their counter and last_used date, and duplicate variants are removed based on the title.
        """
        exam = Exam(exam_name)
        for topic, qtypes in self.structure.items():
            for qtype, qtypecount in qtypes.items():
                qpool = self.qbank[
                    (self.qbank["type"] == qtype) & 
                    (self.qbank["topic"] == topic)
                ]
                qpool = qpool.sample(frac=1)
                qpool = qpool.sort_values(by=["counter","last_used"])
                qpool = qpool.drop_duplicates(subset=["title"], keep="first")
                
                if len(qpool) < qtypecount:
                    raise ValueError(
                        f"Not enough questions of type '{qtype}' "
                        f"for topic '{topic}' available."
                    )

                selected_questions = qpool.head(qtypecount)
                exam.add_questions(selected_questions)
        return exam

    def review_exam(self, exam):
        """Start an interactive review session where the user can approve or modify the exam by replacing questions with other of the same type and topic."""
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
            "\n- If 'yes', question counters and last_used date are going to be updated in the .ssv file,"
            " and the blueprint is going to be exported."
            "\n- If 'no', the proposed exam blueprint is discarded"
            "\n- If 'back', you go back to replacing questions\n").strip().lower()
        if user_input == "yes":
            self.approve_exam(exam)
        elif user_input == "no":
            print("Exam not approved. Blueprint discarded.")
        elif user_input == "back":
            print("Going back to question replacement.")
            self.review_exam(exam)
        else:
            print("Invalid input. Please try again.")
            
    def replace_question(self, exam, index_to_replace):
        """Replace a question in the exam with another question of the same type and topic from the question bank."""
        question_to_replace = exam.questions.iloc[index_to_replace - 1]
        question_pool = self.qbank[
            (self.qbank["type"] == question_to_replace["type"]) &
            (self.qbank["topic"] == question_to_replace["topic"]) &
            (~self.qbank.index.isin(exam.questions.index)) 
        ]
        if question_pool.empty:
            print(f"No replacement question available for "
              f"type '{question_to_replace['type']}' and "
              f"topic '{question_to_replace['topic']}'.")
            return False
        question_pool = question_pool.sort_values(by="counter", ascending=True)
        replacement_question = question_pool.sample(n=1).iloc[0]
        exam.replace_question(index_to_replace - 1, replacement_question)
        
    def approve_exam(self, exam):
        """Approve the exam and update the question bank with the new counters and last_used dates. Export the exam blueprint to a .csv, markdown and .pdf file."""
        exam.export_to_csv()
        exam.export_blueprint_to_markdown()
        exam.export_blueprint_to_pdf()
        self.update_questionbank(exam)
        self.save_questionbank_to_file()
        print("Exam approved and question data updated.")
        print("Exam blueprint and questions exported.")
        
    def update_questionbank(self, exam):
        """Update the counter and last_used date in the question bank for all questions that appear in the approved exam."""
        for index, question in exam.questions.iterrows():
            question_index = self.qbank[
                (self.qbank[["type", "topic", "title", "variant"]] == question[["type", "topic", "title", "variant"]]).all(axis=1)
            ].index[0]
            self.qbank.at[question_index, "counter"] = str(int(self.qbank.at[question_index, "counter"]) + 1)
            self.qbank.at[question_index, "last_used"] = datetime.now().strftime(r"%y%m%d")
        

if __name__ == "__main__":
    import main