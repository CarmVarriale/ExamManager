import pandas as pd
from fpdf import FPDF

QUESTION_PARAMS = [
    "topic", "type", "title", "variant", "counter", "last_used",
    "review_status", "points", "wording", "solution"]

class Exam:
    def __init__(self, name):
        """Initialize the exam with a name and an empty DataFrame 
        for questions."""
        self.name = name
        self.questions = pd.DataFrame(columns=QUESTION_PARAMS)

    def add_questions(self, questions):
        """Add questions to the exam. Questions should be in a Pandas 
        DataFrame format."""
        self.questions = pd.concat(
            [self.questions, questions],
            ignore_index=True)

    def remove_questions(self, indices):
        """Remove questions from the exam on the basis of their indices."""
        if isinstance(indices, int):
            indices = [indices]
        if all(0 <= index < len(self.questions) for index in indices):
            self.questions = self.questions.drop(indices).reset_index(drop=True)
        else:
            raise IndexError(
                "One or more indices are invalid. No questions removed.")

    def replace_question(self, index, new_question):
        """Replace a question at a specific index with a new question."""
        if 0 <= index < len(self.questions):
            self.questions.loc[index] = new_question
        else:
            raise IndexError("Invalid index. No question replaced.")
        
    def get_number_of_questions(self):
        """Get the total number of questions in the exam."""
        return len(self.questions)
    
    def get_total_points(self):
        """Calculate the total points for the exam on the basis of the
        questions and their types."""
        return self.questions['points'].sum()
    
    def export_to_csv(self):
        """Export the exam questions information to a CSV file."""
        filename = f"Exam_{self.name}_Blueprint.csv"
        self.questions.to_csv(filename, sep=';', index=False)
    
    def create_blueprint(self):
        """Create a blueprint dictionary of the exam, categorizing questions 
        by topic and type and collecting information to be printed."""
        blueprint = {}
        for index, question in self.questions.iterrows():
            topic = question['topic']
            type = question['type']
            if topic not in blueprint:
                blueprint[topic] = {}
            if type not in blueprint[topic]:
                blueprint[topic][type] = []
            
            blueprint[topic][type].append({
            "number": index + 1,
            "title": question['title'],
            "variant": question['variant'],
            "wording": question['wording'],
            "solution": question['solution'],
            "points": question['points']
            })
            
        self.blueprint = blueprint

    def print_blueprint(self):
        """Print the exam blueprint to the console."""
        self.create_blueprint()
        print("\nEXAM BLUEPRINT")
        print(f"Exam Name: {self.name}")
        print(f"Total Questions: {self.get_number_of_questions()}")
        print(f"Total Points: {self.get_total_points()}")
        for topic, types in self.blueprint.items():
            print(f"\n{topic}".upper())
            for type, questions in types.items():
                for q in questions:
                    print(f"    Q{q['number']:02} - " +
                          f"{q['title']} {q['variant']} - " +
                          f"{q['points']} Pts")
                    print(f"          {q['wording']} " + 
                          f"(Solution: {q['solution']})")
  
    def export_blueprint_to_markdown(self):  
        """Export the exam blueprint to a Markdown file."""
        self.create_blueprint()
        filename = f"Exam_{self.name}_Blueprint.md"
        with open(filename, 'w') as f:
            f.write("# EXAM BLUEPRINT\n\n")
            f.write(f"Exam Name: {self.name}\n\n")
            f.write(f"Total Questions: {self.get_number_of_questions()}\n\n")
            f.write(f"Total Points: {self.get_total_points()}\n\n")
            for topic, types in self.blueprint.items():
                f.write(f"## {topic.upper()}\n")
                for type, questions in types.items():
                    for q in questions:
                        f.write(f"**Q{q['number']:02} - " + 
                                f"{q['title']} {q['variant']} - " +
                                f"{q['points']} Pts**\n\n")
                        f.write(f"{q['wording']} " +
                                f"*(Solution: {q['solution']})*\n\n")
                        f.write(f"\n\n")

    def export_blueprint_to_pdf(self):
        """Export the exam blueprint to a PDF file."""
        self.create_blueprint()
        pdf = FPDF(format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, 
            txt="EXAM BLUEPRINT", 
            ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, 
            txt=f"Exam Name: {self.name}", 
            ln=True)
        pdf.cell(200, 10,
            txt=f"Total Questions: {self.get_number_of_questions()}",
            ln=True)
        pdf.cell(200, 10, 
            txt=f"Total Points: {self.get_total_points()}", 
            ln=True)
        pdf.ln(10)
        for topic, types in self.blueprint.items():
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(200, 10, 
                txt=topic.upper(), 
                ln=True)
            pdf.set_font("Arial", size=12)
            for type, questions in types.items():
                for q in questions:
                    pdf.multi_cell(0, 10, 
                        txt=f"Q{q['number']:02} - " + 
                        f"{q['title']} {q['variant']} - " +
                        f"{q['points']} Pts - " + 
                        f"{q['wording']}" +
                        f" (Solution: {q['solution']})")
            pdf.ln(5)

        filename = f"Exam_{self.name}_Blueprint.pdf"
        pdf.output(filename)

    def import_from_csv(self, filename):
            """Import questions from a CSV file into the exam."""
            new_questions = pd.read_csv(filename, delimiter=';')
            self.add_questions(new_questions)