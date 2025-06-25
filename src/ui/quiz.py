import os
import random
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer

DATA_DIR = os.path.join("data")
LOGO_PATH = os.path.join("assets", "eigenprep.png")

class QuizWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.setWindowTitle("EigenPrep Quiz Mode")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white;")
        self.main_window = main_window
        self.questions = None
        self.quiz_questions = []
        self.current_question_idx = 0
        self.score = 0
        self.timer = QTimer(self)
        self.time_elapsed = 0
        self.quiz_active = False
        self.was_overridden = False
        self.init_ui()
        self.apply_modern_styling()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(30)
        self.launch_widget = QWidget()
        launch_layout = QVBoxLayout(self.launch_widget)
        launch_layout.setSpacing(20)
        launch_layout.setContentsMargins(0, 0, 0, 0)

        # Logo and title
        logo_row = QHBoxLayout()
        if os.path.exists(LOGO_PATH):
            pixmap = QPixmap(LOGO_PATH).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo = QLabel()
            logo.setPixmap(pixmap)
            logo.setFixedSize(90, 90)
            logo_row.addWidget(logo, alignment=Qt.AlignLeft | Qt.AlignTop)
        else:
            logo = QLabel("EigenPrep")
            logo.setFont(QFont("Segoe UI", 24, QFont.Bold))
            logo_row.addWidget(logo, alignment=Qt.AlignLeft | Qt.AlignTop)
        logo_row.addStretch()
        launch_layout.addLayout(logo_row)

        # Category selection
        self.category_box = QComboBox()
        self.category_box.setFont(QFont("Segoe UI", 13))
        self.category_box.addItem("Select Category...")
        for fname in os.listdir(DATA_DIR):
            if fname.endswith(".csv"):
                self.category_box.addItem(fname.replace(".csv", "").replace("-", " ").title(), fname)
        launch_layout.addWidget(self.category_box)

        # Start button
        self.start_btn = QPushButton("Start Quiz")
        self.start_btn.setFont(QFont("Segoe UI", 14, QFont.Medium))
        self.start_btn.clicked.connect(self.start_quiz)
        launch_layout.addWidget(self.start_btn)

        launch_layout.addStretch()
        self.layout.addWidget(self.launch_widget)

        # Quiz widget (hidden at first)
        self.quiz_widget = QWidget()
        quiz_layout = QVBoxLayout(self.quiz_widget)
        quiz_layout.setSpacing(20)
        quiz_layout.setContentsMargins(0, 0, 0, 0)

        # Timer and progress
        timer_row = QHBoxLayout()
        self.timer_label = QLabel("")
        self.timer_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        timer_row.addWidget(self.timer_label, alignment=Qt.AlignLeft)
        self.progress_label = QLabel("")
        self.progress_label.setFont(QFont("Segoe UI", 13))
        timer_row.addStretch()
        timer_row.addWidget(self.progress_label, alignment=Qt.AlignRight)
        quiz_layout.addLayout(timer_row)

        # Question
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Segoe UI", 15))
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("color: #215bbb; margin-top: 20px; margin-bottom: 10px;")
        quiz_layout.addWidget(self.question_label)

        # Answer input
        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont("Segoe UI", 13))
        self.answer_input.setPlaceholderText("Type your answer here...")
        quiz_layout.addWidget(self.answer_input)

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Segoe UI", 12))
        self.feedback_label.setStyleSheet("color: #16a085; margin-top: 10px;")
        quiz_layout.addWidget(self.feedback_label)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.next_btn = QPushButton("Next Question")
        self.next_btn.setFont(QFont("Segoe UI", 12, QFont.Medium))
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setEnabled(False)
        nav_layout.addWidget(self.next_btn)

        self.submit_btn = QPushButton("Submit Answer")
        self.submit_btn.setFont(QFont("Segoe UI", 12, QFont.Medium))
        self.submit_btn.clicked.connect(self.check_answer)
        self.submit_btn.setEnabled(True)
        nav_layout.addWidget(self.submit_btn)

        self.override_btn = QPushButton("Override: Mark Correct")
        self.override_btn.setFont(QFont("Segoe UI", 12, QFont.Medium))
        self.override_btn.clicked.connect(self.override_correct)
        self.override_btn.setEnabled(False)
        nav_layout.addWidget(self.override_btn)

        self.quit_btn = QPushButton("Quit Quiz")
        self.quit_btn.setFont(QFont("Segoe UI", 12, QFont.Medium))
        self.quit_btn.clicked.connect(self.close)
        nav_layout.addWidget(self.quit_btn)

        quiz_layout.addLayout(nav_layout)
        self.layout.addWidget(self.quiz_widget)
        self.quiz_widget.hide()

        # Connect timer
        self.timer.timeout.connect(self.update_timer)

    def apply_modern_styling(self):
        self.setStyleSheet("""
            QWidget { font-family: 'Segoe UI', Arial, sans-serif; background: white; }
            QComboBox, QLineEdit {
                border: 1.5px solid #215bbb;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 15px;
            }
            QComboBox:focus, QLineEdit:focus {
                border: 2px solid #215bbb;
            }
            QPushButton {
                background: #215bbb;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #3570d1;
            }
            QPushButton:pressed {
                background: #174080;
            }
            QPushButton:disabled {
                background: #bdc3c7; color: #7f8c8d;
            }
        """)

    def start_quiz(self):
        idx = self.category_box.currentIndex()
        if idx == 0:
            QMessageBox.warning(self, "Select Category", "Please select a question category to begin.")
            return
        fname = self.category_box.itemData(idx)
        csv_path = os.path.join(DATA_DIR, fname)
        try:
            questions = pd.read_csv(csv_path)
            if questions.empty:
                raise Exception("No questions found in this category.")
            # Randomly select 5 questions
            if len(questions) < 5:
                self.quiz_questions = questions.sample(len(questions)).reset_index(drop=True)
            else:
                self.quiz_questions = questions.sample(5).reset_index(drop=True)
            self.current_question_idx = 0
            self.score = 0
            self.time_elapsed = 0
            self.quiz_active = True
            self.launch_widget.hide()
            self.quiz_widget.show()
            self.show_question()
            self.timer_label.setText(f"Time: {self.time_elapsed}s")
            self.progress_label.setText(f"Question 1 of {len(self.quiz_questions)}")
            self.timer.start(1000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load questions: {e}")

    def show_question(self):
        q = self.quiz_questions.iloc[self.current_question_idx]
        self.question_label.setText(q['question'])
        self.answer_input.setText("")
        self.answer_input.setEnabled(True)
        self.submit_btn.setEnabled(True)
        self.next_btn.setEnabled(False)
        self.override_btn.setEnabled(False)
        self.was_overridden = False
        self.feedback_label.setText("")
        self.progress_label.setText(f"Question {self.current_question_idx+1} of {len(self.quiz_questions)}")

    def check_answer(self):
        q = self.quiz_questions.iloc[self.current_question_idx]
        user_answer = self.answer_input.text().strip().lower()
        correct_answer = str(q['answer']).strip().lower()
        if user_answer == correct_answer:
            self.feedback_label.setText("✅ Correct!")
            self.score += 1
            self.override_btn.setEnabled(False)
        else:
            self.feedback_label.setText(f"❌ Incorrect. Correct answer: {q['answer']}")
            self.override_btn.setEnabled(True)
        self.submit_btn.setEnabled(False)
        self.next_btn.setEnabled(True)
        self.answer_input.setEnabled(False)

    def override_correct(self):
        if not self.was_overridden:
            self.score += 1
            self.feedback_label.setText(self.feedback_label.text() + "\n✔️ Marked correct by override.")
            self.override_btn.setEnabled(False)
            self.was_overridden = True

    def next_question(self):
        if self.current_question_idx + 1 < len(self.quiz_questions):
            self.current_question_idx += 1
            self.show_question()
        else:
            self.end_quiz()

    def update_timer(self):
        if not self.quiz_active:
            return
        self.time_elapsed += 1
        self.timer_label.setText(f"Time: {self.time_elapsed}s")

    def end_quiz(self):
        self.quiz_active = False
        self.timer.stop()
        msg = QMessageBox(self)
        msg.setWindowTitle("Quiz Complete")
        msg.setText("Quiz Complete!")
        msg.setInformativeText(f"Your score: {self.score} / {len(self.quiz_questions)}\nTime taken: {self.time_elapsed}s")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.close()

    def closeEvent(self, event):
        if self.main_window is not None:
            self.main_window.show()
        super().closeEvent(event) 