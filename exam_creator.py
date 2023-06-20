import os

import openai


def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = f"Create a multiple choice quiz on the topic of {topic} consisting of {num_questions} questions." \
             f"Each question should have {num_possible_answers} options. " \
             f"Also include the correct answer for each question using the starting string 'Correct Answer:'."
    return prompt


if __name__ == '__main__':
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.Completion.create(model='text-davinci-003', prompt=create_test_prompt('Open AI', 4, 4),
                                        max_tokens=256, temperature=0.7)

    print(response['choices'][0]['text'])




