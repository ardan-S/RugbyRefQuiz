from questions.questions import Question, QuestionSet, answer_sets

standard_questions_L6 = QuestionSet("Standard Questions Law 6", [
    # Principle
    Question("""PRINCIPLE: Every match is under the control of match officials who consist of the \\
             referee and two touch judges or assistant referees. Additional persons, as authorised by the \\
             match organisers may include the reserve referee and/or reserve assistant referee, \\
             the television match official, the time-keeper, the match doctor, the team doctors, \\
             the non-playing members of the teams and the ball persons. \\
             Assistant referees and touch judges are responsible for signalling touch, touch \\
             in-goal and the success or otherwise of kicks at goal. In addition, assistant referees \\
             provide assistance as the referee directs, including the reporting of foul play""",
             ["Yes"],
             ["Yes"]),

    # Appointment of the Referee
    Question("Who appoints the referee?",
             answer_sets["answers4"],
             answer_sets["answers4"][0]),

    Question("If no referee has been appointed, how is one chosen?",
             ["By the home team", "By the away team", "By agreement", "Toss of a coin"],
             ["By agreement"]),

    Question("If the referee is unable to complete the match and the match organiser gives no instructions for a replacement, how is one chosen?",
             ["By agreement", "By the referee", "By vote", "The match must end"],
             ["By the referee"]),

    Question("If the referee is unable to complete the match and neither the match organiser nor the referee is able to appoint a replacement, how is one chosen?",
             ["By the home team", "By the away team", "By coin toss", "The match ends"],
             ["By the home team"]),

    # Duties of the Referee Before the Match
    Question("Who organises the toss before the match?",
             ["The team captains", "The match organiser", "The referee", "The assistant referees"],
             ["The referee"]),

    Question("What is the winner of the toss allowed to decide?",
             ["Which side of the field to defend", "Which team gets the first possession", "Whether to kick off or to choose an end", "The duration of the match"],
             ["Whether to kick off or to choose an end"]),

    Question("What must match officials inspect before the match?",
             ["The field", "The players' clothing and studs", "The ball", "The goalposts"],
             ["The players' clothing and studs"]),

    # Duties of the Referee During a Match
    Question("Who is the sole judge of fact and law during a match?",
             ["The team captains", "The match organiser", "The referee", "The assistant referees"],
             ["The referee"]),

    Question("Who keeps the time during a match?",
             ["The match organiser", "The referee", "The assistant referees", "The spectators"],
             ["The referee"]),

    Question("True or false: the match organiser may appoint a time-keeper to signify the end of each half.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("Who permits access to the playing area for players and replacements?",
             ["The team captains", "The match organiser", "The referee", "The assistant referees"],
             ["The referee"]),

    Question("When can a player access water without needing permission?",
             ["During a stoppage", "From their technical area or from behind the dead ball line after a try has been awarded", "While the ball is dead", "Any time during the match"],
             ["From their technical area or from behind the dead ball line after a try has been awarded"]),


    # The Whistle
    Question("When does the referee NOT blow their whistle?",
             ["To indicate the beginning and end of each half", "To stop play", "To indicate score or touchdown", "To caution or send off an offended and again when the penalty or penalty try is awarded", "To restart play after a score"],
             ["To restart play after a score"]),

    Question("When does the referee NOT blow their whistle?",
             ["When the ball becomes dead, other than a failed conversion kick", "When the ball becomes unplayable", "When a penalty, free-kick or scrum is awarded", "When it would be dangerous to let play continue or a serious injury is suspected", "When a substitution is made"],
             ["When a substitution is made"]),

    Question("When does the referee blow the whistle to stop play?",
             ["Only for serious injury", "Only for foul play", "Any time", "When the ball is out of play"],
             ["Any time"]),

    # The Ball Becomes Dead
    Question("When is the ball deemed to be dead?",
             ["When it touches the ground", "When a try is scored", "When the ball is in touch or touch in-goal", "When the referee blows the whistle"],
             ["When the ball is in touch or touch in-goal"]),

    Question("When is the ball NOT deemed to be dead?",
             ["The ball is in touch or touch in-goal", "The ball is grounded in-goal", "A conversion has been attempted", "A dropped goal has been attempted"],
             ["A dropped goal has been attempted"]),

    Question("When is the ball NOT deemed to be dead?",
             ["A try, penalty or dropped goal has been scored", "The ball or ball-carrier touches the dead-ball line or anything beyond it", "The ball hits anything above the playing arena", "The ball is unplayable at a ruck"],
             ["The ball is unplayable at a ruck"]),

    # The ball or ball-carrier touches the referee or non-player
    Question("True or false: if the ball or ball-carrier touches the referee or non-player and either team gains an advantage, play continues.",
             answer_sets["answers6"],
             answer_sets["answers6"][1]),

    Question("True or false: if the ball or ball-carrier touches the referee or non-player and neither team gains an advantage, play continues.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("If the ball touches the referee or other non-player in in-goal and either team gains an advantage, what happens?",
             ["Play continues", "A scrum is awarded", "A try is awarded", "The ball is deemed dead"],
             ["A try is awarded"]),

    # Interaction Between the Referee and Assistant Referees / Touch Judges
    Question("Can the referee consult with assistant referees about matters relating to their duties?",
             answer_sets["answers3"],
             answer_sets["answers3"][0]),

    Question("Which of the following are referees NOT allowed to consult with assistant referees about?",
             ["Matters relating to their duties", "Law relating to foul play", "Timekeeping", "Appointment of captains"],
             ["Appointment of captains"]),

    Question("What can assistant referees and touch judges signal?",
             ["Touch", "Touch in-goal", "Success or failure of kicks at goal", "All of the above"],
             ["All of the above"]),

    Question("True or false: the referee may consult with assistant referees about foul play.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("Who decides if a ball was thrown in from the correct place during a throw-in?",
             ["The referee", "The assistant referees", "The team captains", "The spectators"],
             ["The referee"]),

    Question("True or false: a referee may alter their decision after a touch judge or an assistant referee has raised the flag to signal touch, touch-in-goal or foul play.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    # Television Match Official
    # Law 6.15 and 6.16 skipped

    # Duties of the Referee After the Match
    Question("What must the referee communicate after the match?",
             ["The score", "The weather conditions", "The number of penalties", "The length of each half"],
             ["The score"]),

    Question("If a player was sent off, who must the referee give a written report to?",
             ["The team captain", "The match organiser", "The assistant referees", "The spectators"],
             ["The match organiser"]),

    # Appointing and Controlling Assistant Referees and Touch Judges
    Question("Who provides a touch judge?",
             ["The home team", "The away team", "The referee", "The match organiser"],
             ["The match organiser"]),

    Question("If not appointed by the match organiser, who provides a touch judge?",
             ["The home team", "Each team", "There are no touch judges", "The spectators"],
             ["Each team"]),

    Question("Who nominates a person to act as a replacement for assistant referees and touch judges?",
             ["The referee", "The team captains", "The match organiser", "The spectators"],
             ["The match organiser"]),

    Question("True or false: the referee has control over assistant referees and touch judges.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("True or false: the referee may overrule the decision of an assistant referee or touch judge.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    # During the Match
    Question("Where does the assistant referee or touch judge remain except when judging a kick?",
             ["On the halfway line", "Behind the posts", "In touch", "In the technical area"],
             ["In touch"]),

    Question("Where does the assistant referee or touch judge stand when judging a kick at goal?",
             ["On the halfway line", "Behind the posts", "On the touchline", "In the technical area"],
             ["Behind the posts"]),

    Question("When may an assistant referee enter the playing area to report foul play?",
             ["At any time", "Only when the ball is in play", "At the next stoppage in play and when the referee allows", "Only during half-time"],
             ["At the next stoppage in play and when the referee allows"]),

    # Signals
    Question("What do assistant referees or touch judges use to signal decisions?",
             ["Flags", "Whistles", "Hand signals", "Verbal calls"],
             ["Flags"]),

    Question("How is the success of a kick at goal signaled by an assistant referee or touch judge?",
             ["By raising the flags", "By blowing a whistle", "By waving the flags horizontally", "By verbal call"],
             ["By raising the flags"]),

    Question("Before a throw in and after the ball or ball-carrier has gone into touch, which way does the assistant referee point?",
             ["To the team entitled to throw in", "To the team who took took the ball into touch", "Down the centre of the forming line-out"],
             ["To the team entitled to throw in"]),

    Question("When the ball is thrown in at a line-out, the assistant referee or touch judge lowers the flag with several exceptions. Which of these is NOT an exception?",
             ["The player throwing puts any part of either foot in the field of play", "The team not entitled to throw in has done so", "At quick-throw, the ball that went into touch is replaced by another ball, or touched by another person", "The throw wasn't straight"],
             ["The throw wasn't straight"]),

    Question("Can the assistant referee or touch judge decide if the ball was thrown in from the correct place?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    Question("Can the assistant referee signal foul play",
             ["Yes", "No", "Yes with permission from the referee", "Yes with permission from the match organiser"],
             ["Yes with permission from the match organiser"]),

    Question("How does an assistant referee signal foul play or misconduct has been seen?",
             ["By raising the flag horizontally", "By blowing the whistle", "By waving the flag horizontally", "By verbal call"],
             ["By raising the flag horizontally"]),

    Question("If an assistant referee's verbal report to the referee leads to a player being sent off, what must the assistant referee do after the match?",
             ["Give a written report to the match organiser", "Give a verbal report to the match organiser", "Give a written report to the referee", "Give a verbal report to the referee"],
             ["Give a written report to the referee"]),

    # Additional Persons
    Question("Who can appropriately trained and accredited first-aid or immediate (pitch-side) care persons attend to?",
             ["Any player", "Only players on their team", "The team captain", "The referee"],
             ["Any player"]),

    Question("True or false: medics may enter the playing area to attend to injured players at any time it is safe to do so.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("True or false: medics may not field or touch a ball while it is in live play.",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("When may water carriers enter the playing area?",
             ["During a stoppage in play for an injury or try", "At half-time", "When the referee signals", "At any time"],
             ["During a stoppage in play for an injury or try"]),

    Question("Who must remain in their technical area at all times before entering the field of play?",
             ["The team captains", "The coaches", "Additional persons", "The spectators"],
             ["Additional persons"]),

    Question("When may two nominated water carriers enter the playing area?",
             ["During a stoppage in play for an injury to a player", "When a try has been scored", "At any time", "During a scrum"],
             ["During a stoppage in play for an injury to a player", "When a try has been scored"]),

    Question("Under hot weather guidelines, how long is the break per half for water carriers?",
             ["30 seconds", "1 minute", "2 minutes", "No break"],
             ["1 minute"]),

    Question("In matches with a squad size of 23, when may water carriers enter the field?",
             ["When a try is scored", "During a scrum", "At any stoppage", "During a line-out"],
             ["When a try is scored"]),

    Question("Are water carriers allowed to enter the field at a penalty try?",
             ["Yes", "No", "Only for the scoring team", "Only for the non-scoring team"],
             ["No"]),

    Question("Where may players access water without needing permission from the referee?",
             ["From the Technical zone and behind their own dead ball line", "Anywhere on the field", "From the opposition's Technical zone", "Only from the sidelines"],
             ["From the Technical zone and behind their own dead ball line"]),

    Question("What happens if water is left in-goal?",
             ["The privilege to access water in-goal is removed", "A penalty is awarded", "The water carriers are sent off", "The game is paused"],
             ["The privilege to access water in-goal is removed"]),

    Question("Who must not be a water carrier?",
             ["A substitute player", "A team doctor", "The Head Coach or Director of Rugby", "A team captain"],
             ["The Head Coach or Director of Rugby"]),

    Question("Who may enter the playing area with a kicking tee and one water bottle?",
             ["Any team member", "The Head Coach", "A person designated for the kicker", "A referee"],
             ["A person designated for the kicker"]),

    Question("When may coaches attend to their teams on the field?",
             ["At half-time", "During a penalty", "After a try has been scored", "During a line-out"],
             ["At half-time"]),

    Question("Who may approach or address match officials?",
             ["Coaches", "Water-carriers", "Medics in relation to the treatment of a player", "Spectators"],
             ["Medics in relation to the treatment of a player"])


])


sanction_questions_L6 = QuestionSet("Sanction Questions Law 6", [
    Question("The ball or ball-carrier touches the referee or other non-player and either team gains an advantage in the field of play. Award:",
             ["Scrum to attacking team", "Scrum to team who last played the ball", "Free-kick to attacking team", "Free-kick to team who last played the ball"],
             ["Scrum to team who last played the ball"]),

    Question("The ball-carrier touches the referee or other non-player in in-goal, either team gains an advantage, the ball is in possession of an attacking player. Award:",
             ["5m scrum to attacking team", "5m free-kick to attacking team", "Try where contact took place", "5m scrum to defending team"],
             ["Try where contact took place"]),

    Question("The ball-carrier touches the referee or other non-player in in-goal, either team gains an advantage, the ball is in possession of a defending player. Award:",
             ["5m scrum to defending team", "5m free-kick to defending team", "Touchdown where contact took place", "22m drop-out to defending team"],
             ["Touchdown where contact took place"]),

    # Law 6.12 - skipped

    Question("A medic fields or touches the ball while it is in live play. Sanction:",
             ["Temporary suspension of the medic", "Sending off of the medic", "Penalty where play would restart", "Free-kick where play would restart"],
             ["Penalty where play would restart"]),

    Question("Unauthorized entry or interference by a non-sanctioned person during play: Sanction:",
             ["Warning", "Penalty where play would restart", "Free-kick", "No action"],
             ["Penalty where play would restart"]),

])
