from questions.utils import Question, QuestionSet, answer_sets

standard_questions_L8 = QuestionSet("Standard Questions Law 8", [
    # Value of scoring
    Question("What is the value of a try?",
             ["3 points", "5 points", "7 points", "1 point"],
             ["5 points"]),

    Question("What is the value of a conversion?",
             ["3 points", "5 points", "2 points", "1 point"],
             ["2 points"]),

    Question("What is the value of a penalty try?",
             ["3 points", "5 points", "7 points", "1 point"],
             ["7 points"]),

    Question("What is the value of a penalty goal?",
             ["3 points", "5 points", "7 points", "1 point"],
             ["3 points"]),

    Question("What is the value of a drop goal?",
             ["3 points", "5 points", "7 points", "1 point"],
             ["3 points"]),

    # Try
    Question("Which of these does NOT result in a try?",
             ["A player is the first to ground the ball in the opponents' in-goal", "A player is the first to ground the ball when a scrum, ruck or maul reaches the goal line", "A player is tackled near to the opponents' goal line and the player immediately reaches out and grounds the ball", "A player touches the ball down on the opponents' dead-ball line"],
             ["A player touches the ball down on the opponents' dead-ball line"]),

    Question("If a player is tackled short of the goal line, can their momentum carry them (in a continuous movement) into in-goal where they ground the ball",
             answer_sets["answers3"],
             ["Yes"]),

    Question("Can a player who is in touch or touch-in-goal ground the ball in the opponents' in-goal?",
             ["Yes", "No", "Yes provided the player is not holding the ball", "Yes provided the ball is moving",],
             ["Yes provided the player is not holding the ball"]),

    # Penalty try
    Question("Where is a penalty try awarded",
             ["Under the posts", "At the place of infringement", "At the touchline", "At the place where the ball was last played"],
             ["Under the posts"]),

    Question("When can a penalty try be awarded? (2 correct answers)",
             ["If foul play by the opposing team prevents a probable try from being scored", "If foul play by the opposing team prevents a probable try from being scored in a more advantageous position", "If a legal act prevents a try from being scored in a more advantageous position", "If an act of foul play takes place in in-goal"]
             ["If foul play by the opposing team prevents a probable try from being scored", "If foul play by the opposing team prevents a probable try from being scored in a more advantageous position"]),

    Question("Is a conversion attempted following a penalty try?",
             answer_sets["answers3"],
             ["No"]),

    Question("True or false: A player guilty of foul play which results in the award of a penalty try MUST be cautioned and temporarily suspended or sent off",
             answer_sets["answers3"],
             ["True"]),

    # Conversion, penalty and dropped goal
    Question("Is a conversion successful if it touches a team-mate before passing over the crossbar and between the goal posts?",
             answer_sets["answers3"],
             ["No"]),

    Question("Is a conversion successful if it touches an opponent before passing over the crossbar and between the goal posts?",
             answer_sets["answers3"],
             ["Yes"]),

    Question("Is a conversion successful if it touches the ground before passing over the crossbar and between the goal posts?",
             answer_sets["answers3"],
             ["No"]),

    Question("Is a conversion successful if it goes over the crossbar and over the height of the goal posts but it is deemed that it would have gone between the goal posts had they been taller?",
             answer_sets["answers3"],
             ["Yes"]),

    Question("Does a score stand if the ball has crossed the crossbar and the wind blows it back into the field of play?",
             answer_sets["answers3"],
             ["Yes"]),

    # Conversion
    Question("What type of kick must a conversion be?",
             ["A place kick", "A drop kick", "Either a place or drop kick", "Any kind of kick"],
             ["Either a place or drop kick"]),

    Question("When does a team have the right to attempt a conversion?",
             ["After a try has been scored", "After a penalty try has been awarded", "After a penalty goal has been awarded", "After a drop goal has been scored"],
             ["After a try has been scored"]),

    Question("At a conversion, must the kicker use the ball that was in play when the try was scored?",
             ["Yes", "No", "Yes provided the ball is not defective"],
             ["Yes provided the ball is not defective"]),

    Question("From the following options, where must a conversion be taken?\n1. In the field of play\n2. Through the place where the try was awarded parallel to the touch lines\n3. Behind the 5m line\n4. Within the 15m lines",
             ["1, 2 and 3", "1, 2 and 4", "1 and 2", "1 and 3"],
             ["1 and 2"]),

    Question("What is the ball NOT permitted to be placed on when taking a conversion?",
             ["A kicking tee", "A mound of sand", "A mound of sawdust", "A mound of rubber"],
             ["A mound of rubber"]),

    Question("True or false: at the conversion, the kicker may be assisted by a placer",
             answer_sets["answers3"],
             ["True"]),

    Question("At the conversion, if the ball falls over BEFORE the kicker begins the approach, can the kicker replace it?",
             answer_sets["answers3"],
             ["Yes"]),

    Question("At the conversion, if the ball falls over before the kicker begins the approach and the kicker moves to replace it, can the opponents advance past the goal line?",
             answer_sets["answers3"],
             ["No"]),

    Question("At the conversion, if the ball falls over AFTER the kicker begins the approach, what may the kicker do?",
             ["Replace the ball", "Kick or attempt a dropped goal", "Nothing, the kick is disallowed", "Kick the ball where it landed"],
             ["Kick or attempt a dropped goal"]),

    Question("At the conversion, if the ball falls over and rolls away from the line through the place where the try was awarded, and the kicker kicks the ball over the crossbar, is the conversion successful?",
             answer_sets["answers3"],
             ["Yes"]),

    Question("At the conversion, what are the options for the kicker if the ball falls over and rolls into touch after the kicker begins their approach?",
             ["Kick the ball where it landed", "Replace the ball", "Kick or attempt a dropped goal", "Nothing, the kick is disallowed"],
             ["Nothing, the kick is disallowed"]),

    # The opposing team at a conversion
    Question("At the conversion, where must the opposing team retire to until the kicker begins their approach?",
             ["Behind the 22m", "Behind the 5m", "Behind the try line", "Behind the dead ball line"],
             ["Behind the try line"]),

    Question("At the conversion, in what direction must the kicker move for their approach to the kick to have began?",
             ["Towards the ball", "Towards the goal line", "Towards the touchline", "Any direction"],
             ["Any direction"]),

    Question("At the conversion, after the kicker has began their approach, the opponents may charge. Can they jump to prevent a goal?",
             ["Yes", "No", "Yes provided they are not physically supported by other players"],
             ["Yes provided they are not physically supported by other players"]),

    Question("Is the opposing team permitted to shout during a conversion attempt?",
             answer_sets["answers3"],
             ["No"]),

    Question("At a conversion attempt, the opposing team shouts and the attempt is unsuccessful. A retake is awarded to the kicking team. May the kicker change the type of kick for the second attempt?",
             answer_sets["answers3"],
             ["Yes"]),

    Question("At the conversion, if the ball falls over after the kicker begins the approach to kick, may the opponents continue to charge?",
             answer_sets["answers3"],
             ["Yes"]),

    Question("At the conversion, if the opposition touches the ball and the kick is successful, does the goal stand?",
             answer_sets["answers3"],
             ["Yes"]),

    # Penalty goal
    Question("Can a penalty goal be scored other then from a penalty?",
             answer_sets["answers3"],
             ["No"]),

    Question("How soon must a team indicate their intention to kick for goal?",
             ["Immediately", "Within 30 seconds of the penalty being awarded", "Within 60 seconds of the penalty being awarded", "Without delay"],
             ["Without delay"]),

    Question("If the team indicates to the referee the intention to kick at goal, can they change their decision?",
             answer_sets["answers3"],
             ["No"]),

    Question("Which of these does NOT signal intention to kick at goal?",
             ["Direct communication to the referee", "Arrival of kicking tee or sand", "The player makes a mark on the ground", "The ball is given to the kicker"],
             ["The ball is given to the kicker"]),

    Question("Within what time (playing time) must a penalty goal kick be taken after the team indicated their intention to do so?",
             ["30 seconds", "60 seconds", "90 seconds", "45 seconds"],
             ["60 seconds"]),

    Question("At a penalty goal attempt, what happens to the time permitted to take the kick if the ball rolls over and has to be played again?",
             ["The time is reset", "The time is extended", "The time is reduced", "The time is not affected"],
             ["The time is not affected"]),

])

sanction_questions_L8 = QuestionSet("Sanction Questions Law 8", [
    Question("At a conversion, the kick took longer than 90 seconds however, the ball rolled over and had to be placed again. Sanction?,",
             ["Allow additional time for the kick to be taken", "The kick is disallowed", "The kick is disallowed and play is restarted with a free-kick", "The 90 seconds is reset when the ball rolled over"],
             ["The kick is disallowed"]),

    Question("At a conversion, the kick was not taken within 90 seconds. Sanction?",
             ["Allow additional time for the kick to be taken", "The kick is disallowed, play restarts as normal", "The kick is disallowed and play is restarted with a free-kick", "The kick is disallowed and play is restarted with a penalty"],
             ["The kick is disallowed, play restarts as normal"]),

    Question("At a conversion, members of the kicker's team (excluding a team-mate holding the ball) were in front of the kicker. Sanction?",
             ["The kick is disallowed", "The kick is disallowed and play is restarted with a free-kick", "The kick is disallowed and play is restarted with a penalty", "The kick is retaken"],
             ["The kick is disallowed"]),

    Question("At a conversion, members of the kicker's team misled their opponents into charging too soon. Sanction?",
             ["The kick is disallowed", "The kick is disallowed and play is restarted with a free-kick", "The kick is disallowed and play is restarted with a penalty", "The kick is retaken"],
             ["The kick is disallowed"]),

    Question("During a conversion attempt, the opposing team shouts but the goal is successful. Sanction?",
             ["The score stands", "The kick is disallowed", "A retake is awarded as normal", "A retake is awarded but the opposition must not charge"],
             ["The score stands"]),

    Question("During a conversion attempt, the opposing team shouts and the attempt is unsuccessful. Sanction?",
             ["The score stands", "The kick is disallowed", "A retake is awarded as normal", "A retake is awarded but the opposition must not charge"],
             ["A retake is awarded but the opposition must not charge"]),

    Question("During a penalty goal attempt, the kicker takes longer than 60 seconds (playing time) to take the kick. Sanction?",
             ["The kick is disallowed and a scrum is awarded", "The kick is disallowed and the penalty is reversed", "The kick is retaken"],
             ["The kick is disallowed and a scrum is awarded"]),
])
