import pandas as pd
import random

class QuizEngine:
    def __init__(self, csv_path):
        self.questions = pd.read_csv(csv_path)
        self.current_index = None
        self.asked_indices = set()

    def get_random_question(self, category=None):
        if category:
            filtered = self.questions[self.questions['category'] == category]
        else:
            filtered = self.questions
        available = filtered[~filtered.index.isin(self.asked_indices)]
        if available.empty:
            return None
        idx = random.choice(available.index.tolist())
        self.current_index = idx
        self.asked_indices.add(idx)
        return filtered.loc[idx].to_dict()

    def check_answer(self, user_answer):
        if self.current_index is None:
            return False
        correct = str(self.questions.loc[self.current_index, 'answer']).strip().lower()
        user = str(user_answer).strip().lower()
        return user == correct

    def reset(self):
        self.current_index = None
        self.asked_indices.clear() 