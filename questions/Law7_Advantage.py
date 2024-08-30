from questions.questions import Question, QuestionSet, answer_sets

standard_questions_L7 = QuestionSet("Standard Questions Law 7", [

    Question("If a team gains an advantage following an infringement by their opponents, what may the referee do to keep the game flowing?",
             ["Stop play", "Award a penalty", "Allow play to continue", "Award a free-kick"],
             ["Allow play to continue"]),

    Question("What types of advantage may be allowed?",
             ["Tactical", "Territorial", "Both tactical and territorial", "All of the above"],
             ["All of the above"]),

    Question("What does a tactical advantage allow?",
             ["The non-offending team is free to play the ball as they wish", "Play has moved towards the offending team's dead-ball line", "A combination of tactical and territorial advantage", "A mere opportunity to gain an advantage"],
             ["The non-offending team is free to play the ball as they wish"]),

    Question("What does a territorial advantage allow?",
             ["The non-offending team is free to play the ball as they wish", "Play has moved towards the offending team's dead-ball line", "A combination of tactical and territorial advantage", "A mere opportunity to gain an advantage"],
             ["Play has moved towards the offending team's dead-ball line"]),

    Question("What must the advantage be in order to be applied?",
             ["A mere opportunity to gain an advantage", "Clear and real", "Only tactical", "Only territorial"],
             ["Clear and real"]),

    Question("When does advantage end?",
             ["When the referee deems that the non-offending team has gained an advantage", "When the referee deems that the non-offending team is unlikely to gain an advantage", "When the non-offending team commits an infringement before gaining an advantage", "All of the above"],
             ["All of the above"]),

    Question("What happens if the non-offending team commits an infringement before they have gained an advantage?",
             ["The game continues", "The referee stops the game and applies the sanction for the first infringement", "The referee allows play to continue", "The referee awards a try"],
             ["The referee stops the game and applies the sanction for the first infringement"]),

    Question("What happens if the offending team commits a second or subsequent infringement from which no advantage can be gained?",
             ["The game continues", "The referee allows the captain of the non-offending team to choose the most advantageous sanction", "The referee sanctions the first infringement", "The referee sanctions the second infringement"],
             ["The referee allows the captain of the non-offending team to choose the most advantageous sanction"]),

    Question("When must advantage not be applied and the referee must blow the whistle immediately?",
             ["The ball or a player in possession of the ball, touches the referee and an advantage is gained by either side", "The ball comes out of either end of the tunnel at a scrum", "A scrum is wheeled through more than 90 degrees", "All of the above"],
             ["All of the above"]),

    Question("The ball comes out of either end of the tunnel at a scrum. Sanction?",
             answer_sets["answers1"],
             ["Scrum"]),

    Question("A scrum is wheeled through more than 90 degrees. Can advantage be applied?",
             answer_sets["answers3"],
             ["No"]),

    Question("A quick throw, free-kick or penalty is taken incorrectly. Can advantage be applied?",
             answer_sets["answers3"],
             ["No"]),

    Question("Can advantage be applied if it is suspected that a player is injured?",
             answer_sets["answers3"],
             ["No"]),

])
