import json
import pandas as pd
from fpdf import FPDF

from Question import Question


class Exam:
    def __init__(self, name):
        self.name = name
        self.questions = []
        self.points = self.load_points()

    def load_points(self):
        with open("Points.json", 'r') as f:
            return json.load(f)

    def add_question(self, question):
        self.questions.append(question)

    def replace_question(self, index, new_question):
        self.questions[index] = new_question

    def get_total_points(self):
        total_points = 0
        for question in self.questions:
            total_points += self.points[question.type].get(
                question.topic, 
                self.points[question.type].get("default", 1)
            )
        return total_points

    def get_total_questions(self):
        return len(self.questions)
    
    def print_blueprint(self):
        blueprint = {}
        question_counter = 1
        total_points = self.get_total_points()
        for question in self.questions:
            topic = question.topic
            type = question.type
            if topic not in blueprint:
                blueprint[topic] = {}
            if type not in blueprint[topic]:
                blueprint[topic][type] = []
            blueprint[topic][type].append({
                'wording': question.wording,
                'points': self.points[question.type].get(
                    question.topic, 
                    self.points[question.type].get("default", 1)
                ),
                'number': question_counter
            })
            question_counter += 1

        print("\nEXAM BLUEPRINT\n")
        print(f"Exam Name: {self.name}")
        print(f"Total Questions: {self.get_total_questions()}")
        print(f"Total Points: {total_points}\n")
        for topic, types in blueprint.items():
            print(f"{topic}".upper())
            for type, questions in types.items():
                for q in questions:
                    print(f"    Q{q['number']:02} - {q['points']} Pts - {q['wording']}")

    def to_dict(self):
        return [q.to_dict() for q in self.questions]

    def to_csv(self):
        df = pd.DataFrame(self.to_dict())
        filename = f"Exam_{self.name}_Blueprint.csv"
        df.to_csv(filename, sep=';', index=False)
    
    def to_markdown(self):
        blueprint = {}
        question_counter = 1
        total_points = self.get_total_points()
        for question in self.questions:
            topic = question.topic
            type = question.type
            if topic not in blueprint:
                blueprint[topic] = {}
            if type not in blueprint[topic]:
                blueprint[topic][type] = []
            blueprint[topic][type].append({
                'wording': question.wording,
                'points': self.points[question.type].get(
                    question.topic, 
                    self.points[question.type].get("default", 1)
                ),
                'number': question_counter
            })
            question_counter += 1

        filename = f"Exam_{self.name}_Blueprint.md"
        with open(filename, 'w') as f:
            f.write("# EXAM BLUEPRINT\n\n")
            f.write(f"Exam Name: {self.name}\n\n")
            f.write(f"Total Questions: {self.get_total_questions()}\n\n")
            f.write(f"Total Points: {total_points}\n\n")
            for topic, types in blueprint.items():
                f.write(f"## {topic.upper()}\n")
                for type, questions in types.items():
                    for q in questions:
                        f.write(f"**Q{q['number']:02} - {q['points']} Pts** - {q['wording']}\n\n")

    def to_pdf(self):
        blueprint = {}
        question_counter = 1
        total_points = self.get_total_points()
        for question in self.questions:
            topic = question.topic
            type = question.type
            if topic not in blueprint:
                blueprint[topic] = {}
            if type not in blueprint[topic]:
                blueprint[topic][type] = []
            blueprint[topic][type].append({
                'wording': question.wording,
                'points': self.points[question.type].get(
                    question.topic, 
                    self.points[question.type].get("default", 1)
                ),
                'number': question_counter
            })
            question_counter += 1

        pdf = FPDF(format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="EXAM BLUEPRINT", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Exam Name: {self.name}", ln=True)
        pdf.cell(200, 10, txt=f"Total Questions: {self.get_total_questions()}", ln=True)
        pdf.cell(200, 10, txt=f"Total Points: {total_points}", ln=True)
        pdf.ln(10)
        for topic, types in blueprint.items():
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(200, 10, txt=topic.upper(), ln=True)
            pdf.set_font("Arial", size=12)
            for type, questions in types.items():
                for q in questions:
                    pdf.multi_cell(0, 10, txt=f"Q{q['number']:02} - {q['points']} Pts - {q['wording']}")
            pdf.ln(5)

        filename = f"Exam_{self.name}_Blueprint.pdf"
        pdf.output(filename)

    def from_json(self, exam_file):
        with open(exam_file, 'r') as f:
            data = json.load(f)
        self.name = data["exam_name"]
        self.questions = []
        for q_data in data["questions"]:
            question = Question(
                type=q_data["type"],
                topic=q_data["topic"],
                title=q_data["title"],
                wording=q_data["wording"],
                choices=q_data["choices"],
                solution=q_data["solution"],
                explanation=q_data["explanation"],
                status=q_data["status"],
                counter=q_data["counter"],
                last=q_data["last"]
            )
            self.add_question(question)
