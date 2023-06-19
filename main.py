# This is a sample Python script.
import openai
import os

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(model='text-davinci-003', prompt='Give me two reasons to learn OpenAI API',
                                        max_tokens=300)
    print(response['choices'][0]['text'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
