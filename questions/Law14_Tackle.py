from questions.utils import Question, QuestionSet, answer_sets


sanctionQuestionsL14 = QuestionSet("Sanction Questions", [
    # Law 14: Tackle
    Question("A tackler has not released the ball or the ball-carrier after both players went to ground. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

    Question("A tackler has not immediately moved away from the tackled player and from the ball or got up. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

    Question("A tackler was not on their feet before attempting to play the ball. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0])
])
