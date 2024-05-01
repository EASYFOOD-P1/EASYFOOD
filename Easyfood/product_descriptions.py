#importar librerías
import os
import openai
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv('../openAI.env')
client = OpenAI(
    api_key=os.environ.get('openAI_api_key'),
)

file_path = 'EasyfoodApp/management/commands/db.json'
with open(file_path, 'r') as file:
    file_content = file.read()
    products = json.loads(file_content)


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


instruction = "Vas a actuar como un sistema de recomendacion de comida, que es capaz de darle una detallada descripcion cada plato o producto de comida, describiendo de que se trata, si es o no saludable, si es barato o caro, estas clasificaciones azlas detalladas usando palabras como poco, muy, medianamente, entre otros. añade tambien si la porcion es grande o pequeña,  entre otros atributos para que la descripcion funcione con un sistema de recomendacion de embeding de la api de open ai"


for i in range(len(products)):
    prompt =  f"{instruction} Haz la descripcion para el producto {products[i]['title']} que consiste en {products[i]['description']}"
    response = get_completion(prompt)
    print("-"*30)
    print(response)
    print("-"*30)
    products[i]['sys_description'] = response

file_path1 = "EasyfoodApp/management/commands/db.json"

with open(file_path1, 'w') as json_file:
    json.dump(products, json_file, indent=4)  # The 'indent' parameter is optional for pretty formatting

print(f"Data saved to {file_path}")



