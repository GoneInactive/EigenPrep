import pandas as pd
import random

class OAEngine:
    def __init__(self, csv_path):
        self.questions = pd.read_csv(csv_path)
        self.current_indices = []
        self.answered = {}

    def get_batch(self, n=5, category=None):
        if category:
            filtered = self.questions[self.questions['category'] == category]
        else:
            filtered = self.questions
        available = filtered[~filtered.index.isin(self.current_indices)]
        if len(available) < n:
            n = len(available)
        batch = random.sample(available.index.tolist(), n)
        self.current_indices.extend(batch)
        return [filtered.loc[idx].to_dict() for idx in batch]

    def submit_answer(self, idx, user_answer):
        correct = str(self.questions.loc[idx, 'answer']).strip().lower()
        user = str(user_answer).strip().lower()
        self.answered[idx] = (user, user == correct)
        return user == correct

    def score(self):
        return sum(1 for _, correct in self.answered.values() if correct), len(self.answered)

    def reset(self):
        self.current_indices = []
        self.answered = {} 