# src/chainmind/memory.py

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, question, answer):
        self.history.append({"question": question, "answer": answer})

    def last_n_text(self, n=5):
        text = ""
        for turn in self.history[-n:]:
            text += f"USER: {turn['question']}\nASSISTANT: {turn['answer']}\n\n"
        return text

    def last_answer(self):
        return self.history[-1]["answer"] if self.history else None
