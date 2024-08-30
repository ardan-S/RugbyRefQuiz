import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QPushButton, QButtonGroup, QMessageBox
from questions import all_questions


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.score = 0
        self.question_index = 0
        self.questions = [question for question_set in all_questions for question in question_set.questions]
        self.next_question()

    def initUI(self):
        self.setWindowTitle('Rugby Refereeing Quiz')
        self.layout = QVBoxLayout()

        self.question_label = QLabel("", self)
        self.layout.addWidget(self.question_label)

        self.options_group = QButtonGroup(self)
        self.option_buttons = []
        for _ in range(4):
            btn = QRadioButton("", self)
            self.layout.addWidget(btn)
            self.options_group.addButton(btn)
            self.option_buttons.append(btn)

        self.submit_button = QPushButton("Submit Answer", self)
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def next_question(self):
        if self.question_index < len(self.questions):
            self.display_question(self.questions[self.question_index])
        else:
            self.show_score()

    def display_question(self, question_data):
        self.question_label.setText(question_data.question)
        options = question_data.options[:]
        random.shuffle(options)  # Shuffle the options
        for i, option in enumerate(options):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setChecked(False)

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
            self.question_index += 1
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
