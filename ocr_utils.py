import re

def parse_questions(text):
    lines = text.strip().split("\n")
    questions = []
    current = {}

    for line in lines:
        line = line.strip()
        if re.match(r"^\d+\.", line):
            if current:
                questions.append(current)
                current = {}
            current['question'] = line
            current['answers'] = []
        elif re.match(r"^[A-Da-d]\.", line):
            current['answers'].append((line[0].upper(), line[2:].strip()))

    if current:
        questions.append(current)

    for q in questions:
        q['correct'] = q['answers'][0][0]

    return questions
