import openai
import os
import pandas as pd
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import text


def create_table_definition(df):
    prompt = """###sql Sql table, with properties:
    # 
    # Sales({})
    #
    """.format(",".join(str(col) for col in df.columns))
    return prompt


def prompt_input():
    # nlp_text = input("Enter the info you want: ")
    nlp_text = "return the sum of SALES per POSTALCODE"
    return nlp_text


def combine_prompts(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f'### A query to answer: {query_prompt}\nSELECT'
    return definition+query_init_string


def handle_response(response):
    query = response['choices'][0]['text']
    if query.startswith(' '):
        query = "SELECT" + query
    return query


if __name__ == '__main__':
    openai.api_key = os.getenv('OPENAI_API_KEY')

    df = pd.read_csv('sales_data_sample.csv')

    # Create RAM based DB
    temp_db  = create_engine('sqlite:///:memory:', echo=True)

    # push from pandas to RAM based DB
    df.to_sql(name='Sales', con=temp_db)

    nlp_text = prompt_input()
    prompt = combine_prompts(df, nlp_text)

    response = openai.Completion.create(model='text-davinci-003', prompt=prompt,
                                        temperature=0, max_tokens=150,
                                        top_p=1, frequency_penalty=0, presence_penalty=0,
                                        stop=['#', ';'])

    with temp_db.connect() as conn:
        result = conn.execute(text(handle_response(response)))
        print(result.all())



