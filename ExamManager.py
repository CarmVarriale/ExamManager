import json, random
from os.path import join 
from Question import Question
from Exam import Exam


def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


class ExamManager:
    def __init__(self, exam_database):
        """
        Initialize the ExamManager with the path to the exam database folder.
        The folder should contain the following JSON files:
        - Questions.json
        - Points.json
        - Requirements.json
        """
        self.questions_file = join(exam_database, "Questions.json")
        self.points_file = join(exam_database, "Points.json")
        self.requirements_file = join(exam_database, "Requirements.json")
        self.questions = self.load_questions(self.questions_file)
        self.points = load_json(self.points_file)
        self.requirements = load_json(self.requirements_file)

    def load_questions(self, file):
        data = load_json(file)
        questions = []
        for type, q_list in data.items():
            for question in q_list:
                questions.append(Question(
                    title=question["title"],
                    text=question["text"],
                    solution=question["solution"],
                    topic=question["topic"],
                    explanation=question["explanation"],
                    use_count=question.get("use_count", 0),
                    last_used=question.get("last_used", None),
                    points=question.get("points", 1),
                    type=type,
                    status=question.get("status", "Accepted")
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
                    key=lambda q: q.use_count
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
        exam.to_json()
        exam.to_pdf()
        for question in exam.questions:
            question.increment_use_count()
        self.save_questions()

    def save_questions(self):
        data = {}
        for question in self.questions:
            if question.type not in data:
                data[question.type] = []
            data[question.type].append(question.to_dict())
        save_json(data, self.questions_file)

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