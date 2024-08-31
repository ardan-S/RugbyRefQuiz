from questions.utils import Question, QuestionSet, answer_sets

standard_questions_L3 = QuestionSet("Standard Questions Law 3", [
    # 3.1 Numbers
    Question("How many players can each team have in the playing area during play?",
             ["15", "16", "17", "18", "19", "20"],
             ["15"]),

    Question("Who can authorise matches to be played with fewer than 15 players in each team?",
             answer_sets["answers4"],
             answer_sets["answers4"][0]),

    Question("Number of replacements for international matches?",
             ["6", "7", "8", "14", "10", "12"],
             ["8"]),

    Question("For non international matches, who decides the number of replacements (to a maximum of eight)?",
             answer_sets["answers4"],
             answer_sets["answers4"][0]),

    Question("Can replacements be made if the ball is not dead?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    Question("Can replacements be made without the permission of the referee?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    Question("What is the minimum number of front row players required for a squad size of 15 or fewer?",
             ["1", "2", "3", "4", "5", "6"],
             ["3"]),

    Question("What is the minimum number of front row players required for a squad size of 16, 17 or 18?",
             ["1", "2", "3", "4", "5", "6"],
             ["4"]),

    Question("What is the minimum number of front row players required for a squad size of 19 to 22?",
             ["1", "2", "3", "4", "5", "6"],
             ["5"]),

    Question("What is the minimum number of front row players required for a squad size of 23?",
             ["1", "2", "3", "4", "5", "6"],
             ["6"]),

    Question("Who must a squad size of 16, 17 or 18 be able to replace at the first time of asking?",
             answer_sets["answers5"],
             answer_sets["answers5"][0]),

    Question("Who must a squad size of 19 to 22 be able to replace at the first time of asking?",
             answer_sets["answers5"],
             answer_sets["answers5"][1]),

    Question("Who must a squad size of 23 be able to replace at the first time of asking?",
             answer_sets["answers5"],
             answer_sets["answers5"][2]),

    Question("Where the match organiser has determined squad sizes of 23 and a team is able to nominate only two front-row replacements, how many players may be nominated to their squad?",
             ["21", "22", "23"],
             ["22"]),

    Question("True or false: prior to the match, each time must advise the appropriate match official of their front-row and possible front-row replacements?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("True or false: a player not originally advertised as a front-row replacement may replace a front-row player in the case of injury?",
             answer_sets["answers6"],
             answer_sets["answers6"][1]),

    Question("True or false: a replacement front-row player may start the match in another position?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    # 3.2 Uncontested scrums
    Question("Under what circumstances do scrums become uncontested? (2 correct answers)",
             ["Either team cannot field a suitably trained front row", "The referee orders so", "Both teams agree", "All of the above"],
             ["Either team cannot field a suitably trained front row", "The referee orders so"]),

    Question("True or false: a match organiser may stipulate conditions under which a game may start with uncontensted scrums?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("How many players per side must play in an uncontested scrum which resulted from a sending off, temporary suspension or injury?",
             ["3", "5", "6", "7", "8"],
             ["8"]),

    Question("Weather through injury, temporary or permanent suspension, a front-row player leaves the playing area. At the next scrum, the referee is informed the team will not be able to contest the scrum. What must the referee do?",
             ["Ask for another player to join the scrum", "Order uncontested scrums", "Play with that position in the scrum vacant"],
             ["Order uncontested scrums"]),

    Question("If uncontested scrums have been ordered but a front-row player comes on, may contested scrums continue?",
             answer_sets["answers3"],
             answer_sets["answers3"][0]),

    Question("In a squad of 23, or at the discretion of the match organiser, can a player whose departure has caused the referee to order uncontested scrums be replaced?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    Question("Can a non-front-row player play in the front row if a front-row player is available?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    Question("True or false: if a front-row player is temporarily suspended, and the team cannot continue with contested scrums with the players on the field, the team nominates a player to leave the playing area to enable an available front-row player to come on. The nominated player may not return until the suspension period ends?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("True or false: if a front-row player is sent off, and the team cannot continue with contested scrums with the players on the field, the team nominates a player to leave the playing area to enable an available front-row player to come on. The nominated player may return until the end of the match?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    # Permanent replacement
    Question("True or false: an injured player may return having been replaced?",
             answer_sets["answers6"],
             answer_sets["answers6"][1]),

    Question("Under which of these conditions is a player NOT deemed to be injured?",
             ["At national level, it is the opinion of a doctor that it would be inadvisable for the player to continue", "In other matches, where a match organiser has given explicit permission, it is the opinion of a medically trained person that it would be inadvisable for the player to continue. If none is present, the player may be replaced if the referee agrees",
              "The referee decides (with or without medical advice) that it would be inadvisable for the player to continue", "It is the opinion of the team captain that it would be inadvisable for the player to continue"],
             ["It is the opinion of the team captain that it would be inadvisable for the player to continue"]),

    Question("True or false: a referee may order an injured player to leave the playing area to be medically examined?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    # Permanent replacement - recognise and remove
    Question('What is the process known as "Recognise and Remove"?',
             ["Immediate and permanent removal of a blood injury", "Immediate and permanent removal of a player who has committed an act of foul play", "Immediate and permanent removal of a player who is concussed or has suspected concussion", "Immediate and permanent removal of a player not deemed to be of sufficient standard"],
             ["Immediate and permanent removal of a player who is concussed or has suspected concussion"]),

    # Temporary replacement - blood injury
    Question("True or false: a player with a blood injury may be temporarily replaced?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("A player with a blood injury is replaced. How long does the replacement have to return to the field before the replacement becomes permenant?",
             ["5 minutes", "10 minutes", "15 minutes", "20 minutes", "25 minutes", "30 minutes"],
             ["15 minutes"]),

    # Point 26 skipped for relevance (blood injury in international matches)

    # Point 27 skipped for relevance (HIA in approved matches)

    # Temporary replacement - all
    Question("True or false: a temporary replacement can be temporarily replaced, even if all replacements have been used?",
             answer_sets["answers6"],
             answer_sets["answers6"][0]),

    Question("If a temporary replacement is injured, can they be replaced?",
             answer_sets["answers3"],
             answer_sets["answers3"][0]),

    Question("If a temporary replacement is sent off can the originally replaced player return to the playing area?",
             ["Yes", "No", "No with 2 lawful exceptions", "Yes with 2 lawful exceptions"],
             ["No with 2 lawful exceptions"]),

    Question("If the time allowed for a temporary replacement elapses during half-time, can the replaced player return?",
             ["No", "The time continues after the second half begins", "Only if replaced player returns immediately at the start of the second half", "The replacement is replaced, then the original player may return"],
             "Only if replaced player returns immediately at the start of the second half"),

    # Tactical replacements joining the match
    Question("Which is NOT a valid reason for a tactically replaced player to return to the playing area? When replacing:",
             ["An injured front-row player", "A player with a blood injury", "A player with a head injury", "A player who has been injured as a result of foul play", "A nominated player described in Law 3.19 or 3.20", "The captain to come on as captain"],
             ["The captain to come on as captain"]),

    # Rolling replacements
    Question("Who is responsible for implementing rolling tactical replacements?",
             answer_sets["answers4"],
             answer_sets["answers4"][0]),

    Question("What is the maximum number of rolling tactical replacements allowed?",
             ["8", "10", "12", "14", "16", "18"],
             ["12"]),

])


sanction_questions_L3 = QuestionSet("Sanction Questions Law 3", [
    Question("A team has too many players in the playing area during play. The referee orders the captain to reduce the number of players. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

    Question("A team has too many players in the playing area during play. The referee orders the captain to reduce the number of players. Adjustment to the score:",
             ["Reduced by a try (5 pts)", "Reduced by a penalty (3 pts)", "No change", "Reduced by a conversion (2 pts)"],
             ["No change"]),

    Question("A player or replacement rejoins the match without the referee's permission. The referee believes the player did so to gain an advantage. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

])
