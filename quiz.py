import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QPushButton, QButtonGroup, QMessageBox, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont

from questions.Law1_TheGround import standard_questions_L1
from questions.Law3_Team import standard_questions_L3, sanction_questions_L3
from questions.Law4_PlayersClothing import standard_questions_L4, sanction_questions_L4
from questions.Law5_Time import standard_questions_L5
from questions.Law6_MatchOfficials import standard_questions_L6, sanction_questions_L6
from questions.Law7_Advantage import standard_questions_L7

all_questions = [standard_questions_L1,
                 standard_questions_L3, sanction_questions_L3,
                 standard_questions_L4, sanction_questions_L4,
                 standard_questions_L5,
                 standard_questions_L6, sanction_questions_L6,
                 standard_questions_L7]


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.score = 0
        self.question_index = 0
        self.questions = [question for question_set in all_questions for question in question_set.questions]
        self.asked_questions_idxs = []
        self.next_question()


    def initUI(self):
        self.setWindowTitle('Rugby Refereeing Quiz')
        self.resize(1000, 600)
        self.center()
        self.layout = QVBoxLayout()

        self.question_label = QLabel("", self)
        self.layout.addWidget(self.question_label)

        self.options_group = QButtonGroup(self)
        self.option_buttons = []

        self.submit_button = QPushButton("Submit Answer", self)
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)


    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def next_question(self):
        if self.question_index < len(self.questions):
            self.display_question(self.questions[self.question_index])
        else:
            self.show_score()


    def display_question(self, question_data):
        question_font = QFont("Arial", 18)
        option_font = QFont("Arial", 14)

        self.question_label.setFont(question_font)
        self.question_label.setText(question_data.question)
        
        options = question_data.options[:]
        random.shuffle(options)
        
        # Clear any existing option buttons
        for btn in self.option_buttons:
            self.options_group.removeButton(btn)
            btn.deleteLater()

        self.option_buttons = []
        grid_layout = QGridLayout()
        button_width = 200
        rows = (len(options) + 1) // 2
        
        # Create new buttons based on the number of options
        for i, option in enumerate(options):
            btn = QRadioButton(option, self)
            btn.setFont(option_font)
            self.layout.insertWidget(self.layout.count() - 1, btn)
            self.options_group.addButton(btn)
            self.option_buttons.append(btn)

            row = i % rows
            col = i // rows
            grid_layout.addWidget(btn, row, col)

        hbox_layout = QHBoxLayout()
        hbox_layout.addStretch(1)
        hbox_layout.addLayout(grid_layout)
        hbox_layout.addStretch(1)

        self.layout.insertLayout(self.layout.count() - 1, hbox_layout)

    def check_answer(self):
        selected_button = self.options_group.checkedButton()
        if selected_button:
            selected_option = selected_button.text()
            correct_answers = self.questions[self.question_index].answers
            if selected_option in correct_answers:
                self.score += 1
                QMessageBox.information(self, "Correct!", "Your answer is correct!")
            else:
                QMessageBox.information(self, "Wrong!", f"Correct answer(s): {', '.join(correct_answers)}")
            self.asked_questions_idxs.append(self.question_index)
            while self.question_index in self.asked_questions_idxs:
                self.question_index = random.randint(0, len(self.questions) - 1)
            self.next_question()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an option!")


    def show_score(self):
        QMessageBox.information(self, "Quiz Completed", f"Your score is {self.score}/{len(self.questions)}")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec_())
