from questions.utils import Question, QuestionSet, answer_sets

standard_questions_L1 = QuestionSet("Standard Questions Law 1", [

    Question("Which of the following is NOT permitted surface types?",
             ["Grass", "Artificial turf", "Sand", "Concrete", "Clay", "Snow"],
             ["Concrete"]),

    Question("What is the maximum length of the field of play?",
             ["100m", "96m", "104m", "106m", "94m", "90m"],
             ["100m"]),

    Question("What is the maximum width of the field of play?",
             ["64m", "66m", "70m", "72m", "68m", "74m"],
             ["70m"]),

    Question("What is the maximum length of the in-goal area?",
             ["12m", "15m", "20m", "22m", "25m", "30m"],
             ["22m"]),

    Question("What is the minimum length of the field of play?",
             ["92m", "94m", "96m", "100m", "88m", "90m"],
             ["94m"]),

    Question("What is the minimum width of the field of play?",
             ["64m", "66m", "70m", "72m", "68m", "74m"],
             ["68m"]),

    Question("What is the minimum length of the in-goal area?",
             ["6m", "8m", "10m", "12m", "14m", "16m"],
             ["6m"]),

    Question("Where the length of the field of play is less than 100m, which section of the pitch is reduced accordingly?",
             ["Goal line - 22m", "22m - 10m", "10m - Halfway", "In-goal area"],
             ["22m - 10m"]),

    Question("Where the width of the field of play is less than 70m, which section of the pitch is reduced accordingly?",
             ["Touch line - 5m", "5m - 15m", "15m - 15m"],
             ["15m - 15m"]),

    Question("Where practicable, what is the minimum length of the perimiter area?",
             ["2m", "3m", "4m", "5m", "6m", "7m"],
             ["5m"]),

    Question("Which configuration of lines are on the dead-ball and touch-in-goal lines?",
             answer_sets["answers2"],
             answer_sets["answers2"][0]),

    Question("Which configuration of lines are on the goal lines?",
             answer_sets["answers2"],
             answer_sets["answers2"][0]),

    Question("Which configuration of lines are on the 22m lines?",
             answer_sets["answers2"],
             answer_sets["answers2"][0]),

    Question("Which configuration of line is on the half-way line?",
             answer_sets["answers2"],
             answer_sets["answers2"][0]),

    Question("Which configuration of lines are on the touchlines?",
             answer_sets["answers2"],
             answer_sets["answers2"][0]),

    Question("Which configuration of lines are 5m from, and parallel to each touchline?",
             answer_sets["answers2"],
             answer_sets["answers2"][1]),

    Question("Which configuration of lines are 15m from, and parallel to each touchline?",
             answer_sets["answers2"],
             answer_sets["answers2"][1]),

    Question("Which configuration of lines are 10m from, and parallel to each side of the half-way?",
             answer_sets["answers2"],
             answer_sets["answers2"][1]),

    Question("Which configuration of lines are 5m from, and parallel to each goal line?",
             answer_sets["answers2"],
             answer_sets["answers2"][1]),

    Question("How long is the single line which intersects the centre of the half-way line?",
             ["0.2m", "0.3m", "0.4m", "0.5m", "0.6m", "0.7m"],
             ["0.5m"]),

    Question("How may flag posts are on the pitch?",
             ["8", "10", "12", "14", "16", "6"],
             ["14"]),

    Question("Where are each of the 14 flag posts located?",
             ["I know where each one is"],
             ["I know where each one is"]),

    Question("Can the team inform the referee of any objections to the ground after the match starts?",
             answer_sets["answers3"],
             answer_sets["answers3"][1]),

])
