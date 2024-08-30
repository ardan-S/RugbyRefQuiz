from questions.questions import Question, QuestionSet, answer_sets

standard_questions_L5 = QuestionSet("Standard Questions Law 5", [
    # 5.1 Match Duration
    Question("How long does a match last?",
             ["80 minutes", "90 minutes", "70 minutes", "60 minutes"],
             ["80 minutes"]),

    Question("How long can each half last?",
             ["30 minutes", "35 minutes", "40 minutes", "45 minutes"],
             ["40 minutes"]),

    Question("What is the maximum duration for half-time?",
             ["10 minutes", "12 minutes", "15 minutes", "20 minutes"],
             ["15 minutes"]),

    Question("Who decides the length of the half-time interval?",
             answer_sets["answers4"],
             answer_sets["answers4"][0]),

    # 5.2 Non-international Matches
    Question("In non-international matches, who can decide to reduce the length of the match?",
             answer_sets["answers4"],
             answer_sets["answers4"][0]),

    Question("If the match organiser does not decide the length of a non-international match, who agrees on the length?",
             ["The captains", "The coaches", "The referees", "The spectators"],
             ["The captains"]),

    # 5.3 Referee's Role
    Question("Who keeps the time during a match?",
             ["The match organiser", "The referee", "The assistant referees", "The timekeeper"],
             ["The referee"]),

    Question("True or false: the referee can delegate timekeeping duties to an official timekeeper.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("Who may the referee consult if there is doubt about the correct time?",
             ["The captains", "The coaches", "The assistant referees and official timekeeper", "The spectators"],
             ["The assistant referees and official timekeeper"]),

    # 5.4 Stopping Play
    Question("How long may the referee allow for a player injury?",
             ["Up to 30 seconds", "Up to 1 minute", "Up to 2 minutes", "Up to 5 minutes"],
             ["Up to 1 minute"]),

    Question("What can the referee do if a player is seriously injured?",
             ["Stop the match permanently", "Call for a stretcher", "Allow more than one minute for the player to be removed", "Continue the match"],
             ["Allow more than one minute for the player to be removed"]),

    Question("What are the situations in which the referee may allow time once the ball is dead?",
             ["Replacement of players", "Replacing or repairing players' clothing", "Re-tying a boot-lace", "Retrieving the ball", "All of the above"],
             ["All of the above"]),

    # 5.5 Ending a Half
    Question("When does a half end after time has expired?",
             ["When the ball goes out of play", "When the referee blows the whistle", "When the ball becomes dead", "When a try is scored"],
             ["When the ball becomes dead"]),

    Question("Which of the following does NOT cause the half to end after time has expired?",
             ["A scrum, lineout or restart kick following a try or touchdown", "A penalty kick into touch without the ball first being tapped", "A try being scored", "A knock-on"],
             ["A knock-on"]),

    Question("True or false: a team scoring a try may decline the conversion.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    # 5.6 Water Breaks
    Question("When can the referee allow a water break?",
             ["At half-time", "When a player is injured", "When the weather conditions are exceptionally hot and/or humid", "Any time during the match"],
             ["When the weather conditions are exceptionally hot and/or humid"]),

    Question("How long is the water break?",
             ["30 seconds", "1 minute", "2 minutes", "5 minutes"],
             ["1 minute"]),

    # 5.7 Referee's Authority
    Question("What power does the referee have regarding ending or suspending the match?",
             ["No power", "Only in case of foul play", "Only if the match is drawn", "To end or suspend the match if it is unsafe to continue"],
             ["To end or suspend the match if it is unsafe to continue"])
])
