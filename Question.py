from datetime import datetime


def validate_input(value, valid_set, name):
    if value not in valid_set:
        raise ValueError(f"Invalid {name} '{value}'. Valid {name}s are: {', '.join(valid_set)}")
    return value

def validate_date(date_str):
    try:
        datetime.strptime(date_str, r'%y%m%d')
    except ValueError:
        raise ValueError(f"Invalid date '{date_str}'. Date must be in YYMMDD format.")
    return date_str

class Question:
    VALID_STATUSES = {"accepted", "review_needed", "revision_needed"}
    VALID_TYPES = {"true_false", "multiple_choice", "numerical"}

    def __init__(self, type, topic, title, wording, choices, solution, explanation, status, counter=0, last=None):
        self.type = validate_input(type, self.VALID_TYPES, "type")
        self.topic = topic
        self.title = title
        self.wording = wording
        self.choices = choices
        self.solution = solution
        self.explanation = explanation
        self.status = validate_input(status, self.VALID_STATUSES, "status")
        self.counter = counter
        self.last = validate_date(last) if last else datetime.now().strftime(r'%y%m%d')

    def increment_counter(self):
        self.counter += 1
        self.last = datetime.now().strftime(r'%y%m%d')

    def to_dict(self):
        return {
            "type": self.type,
            "topic": self.topic,
            "title": self.title,
            "wording": self.wording,
            "choices": self.choices,
            "solution": self.solution,
            "explanation": self.explanation,
            "status": self.status,
            "counter": self.counter,
            "last": self.last
        }
