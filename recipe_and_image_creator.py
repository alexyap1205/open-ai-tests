import shutil

import openai
import os
import re
import requests


def create_dish_prompt(list_of_ingredients):
    prompt = f"Create a detailed recipe based on only the following ingredients: {'. '.join(list_of_ingredients)}.\n" \
                + "Additionally, assign a title starting with 'Recipe Title: ' to this recipe."
    return prompt


def extract_title(recipe):
    return re.findall('^.*Recipe Title: .*$', recipe, re.MULTILINE)[0].split('Recipe Title: ')[-1]


def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream=True)
    if image_res.status_code == 200:
        image_res.raw.decode_content = True
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print('Image couldn\'t be retreived')

    return image_res.status_code


def dalle2_prompt(recipe_title):
    prompt = f"{recipe_title}, professional food photography, 15mm, studio lighting"
    return prompt


if __name__ == '__main__':
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.Completion.create(engine='text-davinci-003',
                                        prompt=create_dish_prompt(['chicken', 'lemongrass', 'thyme', 'carrots', 'onions',
                                                                   'garlic', 'salt', 'pepper', 'olive oil']),
                                        temperature=0.7, max_tokens=512)
    result_text = response['choices'][0]['text']

    title = extract_title(result_text)
    print(result_text)

    image_respose = openai.Image.create(prompt=dalle2_prompt(title),
                                        n=1,
                                        size='1024x1024')

    print(image_respose['data'][0]['url'])
    save_image(image_respose['data'][0]['url'], f'{title}.png')
