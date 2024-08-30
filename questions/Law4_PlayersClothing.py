from questions import Question, QuestionSet, answer_sets

standard_questions_L4 = QuestionSet("Standard Questions Law 4", [
    # 4.1 General Requirements
    Question("All items of clothing must comply with which regulation?",
             ["World Rugby Regulation 10", "World Rugby Regulation 11", "World Rugby Regulation 12", "World Rugby Regulation 13"],
             ["World Rugby Regulation 12"]),

    Question("What must a player wear during a match?",
             ["Jersey, shorts, underwear, socks, and boots", "Jersey, shorts, socks, and boots", "Jersey, shorts, and socks", "Jersey, shorts, and boots"],
             ["Jersey, shorts, underwear, socks, and boots"]),

    Question("How far must the sleeve of a jersey extend?",
             ["To the wrist", "To the elbow", "At least halfway from the shoulder point to the elbow", "To the shoulder point"],
             ["At least halfway from the shoulder point to the elbow"]),

    # 4.3 Additional Items Permitted
    Question("True or false: a player can wear ankle supports extending halfway up the shin?",
             answer_sets["answers6"],
             answer_sets["answers6"][1]),

    Question("Which of the following items is not allowed?",
             ["Fingerless gloves", "Jewellery", "Mouth guard", "Goggles"],
             ["Jewellery"]),

    Question("What must a headscarf or covering ensure?",
             ["It looks good", "It does not cause a danger to the wearer or other players", "It matches the team color", "It is made of cotton"],
             ["It does not cause a danger to the wearer or other players"]),

    # 4.4 Prohibited Items
    Question("A player may not wear any item contaminated by:",
             ["Water", "Mud", "Blood", "Sweat"],
             ["Blood"]),

    Question("Can a player wear gloves?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    Question("What type of boots studs are permitted?",
             ["Metal studs only", "Plastic studs only", "Studs made of moulded rubber", "Studs of any material"],
             ["Studs made of moulded rubber"]),

    Question("True or false: a player may wear shorts or leggings with padding sewn into them?",
             answer_sets["answers6"],
             answer_sets["answers6"][1]),

    Question("Can a player wear communication devices?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

    # 4.5 Referee's Authority
    Question("Who has the power to decide if a player's clothing is dangerous or illegal during a match?",
             answer_sets["answers4"],
             answer_sets["answers4"][2]),

    Question("What must a player do if the referee orders the removal of an item of clothing?",
             ["Ignore the referee", "Remove the item and continue playing", "Remove the item or render it harmless", "Complain to the referee"],
             ["Remove the item or render it harmless"]),

    Question("What is the sanction for a player found wearing a banned item during play after being warned?",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

    Question("Under what condition can a player leave the playing area to change items of clothing?",
             ["Any time during the match", "Only if approved by the referee", "If they are bloodstained", "At half-time"],
             ["If they are bloodstained"])
])

sanction_questions_L4 = QuestionSet("Sanction Questions Law 4", [
    Question("A player wears an item of clothing deemed illegal by the referee during the match. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

    Question("A player is found wearing a prohibited item after being warned by the match official. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0]),

    Question("A player leaves the playing area to change a non-bloodstained item of clothing. Sanction:",
             answer_sets["answers1"],
             answer_sets["answers1"][0])
])
