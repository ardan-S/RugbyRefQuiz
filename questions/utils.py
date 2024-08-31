class Question:
    def __init__(self, question, options, answers):
        self.question = question
        self.options = options
        self.answers = answers


class QuestionSet:
    def __init__(self, name, questions):
        self.name = name
        self.questions = questions


answer_sets = {
    "answers1": ['Penalty', 'Free kick', 'Scrum', 'Play advantage', 'Other'],
    "answers2": ['Solid', 'Dashed'],
    "answers3": ['Yes', 'No'],
    "answers4": ['The match organiser', 'The governing body', 'The referee', 'World Rugby'],
    "answers5": ['Either a prop or a hooker', 'Both a prop and a hooker', 'Loose-head, tight-head and hooker'],
    "answers6": ['True', 'False']
}


