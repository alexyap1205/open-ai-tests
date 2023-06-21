import os

import openai


def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = f"Create a multiple choice quiz on the topic of {topic} consisting of {num_questions} questions." \
             f"Each question should have {num_possible_answers} options. " \
             f"Also include the correct answer for each question using the starting string 'Correct Answer:'."
    return prompt


def create_student_view(test, num_questions):
    student_view = {1: ''}
    question_number = 1
    for line in test.splitlines():
        if not line.startswith('Correct Answer:'):
            student_view[question_number] += line + '\n'
        else:
            if question_number < num_questions:
                question_number += 1
                student_view[question_number] = ''
    return student_view


def extract_answer(test, num_questions):
    answers = {1: ''}
    question_number = 1
    for line in test.splitlines():
        if line.startswith('Correct Answer:'):
            answers[question_number] += line + '\n'
            if question_number < num_questions:
                question_number += 1
                answers[question_number] = ''
    return answers


def take_exam(student_view):
    student_answers = {}
    for question, question_view in student_view.items():
        print(student_view[question])
        answer = input('Enter your answer: ')
        student_answers[question] = answer
    return student_answers


def grade_exam(correct_answers, student_answers):
    correct_answer_count = 0
    for question, answer in student_answers.items():
        if answer.upper() == correct_answers[question][16]:
            correct_answer_count += 1

    grade = 100 * correct_answer_count / len(correct_answers)
    if grade < 60:
        print(f'You failed the exam with a grade of {grade}%.')
    else:
        print(f'You passed the exam with a grade of {grade}%.')

    return grade


if __name__ == '__main__':
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.Completion.create(model='text-davinci-003', prompt=create_test_prompt('Australia History', 4, 4),
                                        max_tokens=256, temperature=0.7)

    student_view = create_student_view(response['choices'][0]['text'], 4)
    # for key in student_view:
    #     print(student_view[key])

    answers = extract_answer(response['choices'][0]['text'], 4)
    # for answer in answers:
    #     print(answers[answer])

    student_answers = take_exam(student_view)
    grade_exam(answers, student_answers)





