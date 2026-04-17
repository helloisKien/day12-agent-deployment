def ask(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please provide a question."
    return f"[Mock answer] You asked: {question}"
