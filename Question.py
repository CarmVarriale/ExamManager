from datetime import datetime

class Question:
    VALID_STATUSES = {"Accepted", "Review Needed", "Revision Needed"}
    VALID_TYPES = {"true_false", "multiple_choice", "numerical"}

    @staticmethod
    def validate_input(value, valid_set, name):
        if value not in valid_set:
            raise ValueError(f"Invalid {name} '{value}'. Valid {name}s are: {', '.join(valid_set)}")
        return value

    def __init__(self, title, text, solution, topic, explanation, 
                 use_count=0, last_used=None, points=1, type="true_false", status="Review Needed"):
        self.title = title
        self.text = text
        self.solution = solution
        self.topic = topic
        self.explanation = explanation
        self.use_count = use_count
        self.last_used = last_used
        self.points = points
        self.type = self.validate_input(type, self.VALID_TYPES, "type")
        self.status = self.validate_input(status, self.VALID_STATUSES, "status")

    def increment_use_count(self):
        self.use_count += 1
        self.last_used = datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "text": self.text,
            "solution": self.solution,
            "topic": self.topic,
            "explanation": self.explanation,
            "use_count": self.use_count,
            "last_used": self.last_used,
            "points": self.points,
            "type": self.type,
            "status": self.status
        }
