from dotenv import load_dotenv, find_dotenv
import json
import os
import openai
from openai import OpenAI
import numpy as np

_ = load_dotenv('../openAI.env')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('openAI_api_key'),
)
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



# Ruta al archivo JSON
json_file_path = 'EasyfoodApp/management/commands/db.json'

# Abrir el archivo JSON y cargar su contenido
with open(json_file_path, 'r') as file:
    file_content = file.read()
    products = json.loads(file_content)

#Esta función devuelve una representación numérica (embedding) de un texto, en este caso
#la descripción de las películas
emb = get_embedding(products[1]['description'])
#print(emb)

#Vamos a crear una nueva llave con el embedding de la descripción de cada película en el archivo .json


for i in range(len(products)):
  emb = get_embedding(products[i]['description'])
  products[i]['embedding'] = emb



# Write the data to the JSON file
with open('EasyfoodApp/management/commands/embeddings_db.json', 'w') as json_file:
    json.dump(products, json_file, indent=4)  # The 'indent' parameter is optional for pretty formatting

print(f"Data saved to emb_json")



"""
print(products[0])

#Para saber cuáles películas se parecen más, podemos hacer lo siguiente:
print(products[0]['title'])
print(products[1]['title'])
print(products[2]['title'])

#Calculamos la similitud de coseno entre los embeddings de las descripciones de las películas. Entre más alta la similitud
#más parecidas las películas.

print(f"Similitud entre película {products[0]['title']} y {products[1]['title']}: {cosine_similarity(products[0]['embedding'],products[1]['embedding'])}")
print(f"Similitud entre película {products[0]['title']} y {products[2]['title']}: {cosine_similarity(products[0]['embedding'],products[2]['embedding'])}")
print(f"Similitud entre película {products[2]['title']} y {products[1]['title']}: {cosine_similarity(products[2]['embedding'],products[1]['embedding'])}")

#Si se tuviera un prompt por ejemplo: Película de la segunda guerra mundial, podríamos generar el embedding del prompt y comparar contra 
#los embeddings de cada una de las películas de la base de datos. La película con la similitud más alta al prompt sería la película
#recomendada.

"""
req = "quiero comer algo que tenga pollo y salsa pero que no sea una hamburguesa "
emb = get_embedding(req)

sim = []
for i in range(len(products)):
  sim.append(cosine_similarity(emb,products[i]['embedding']))
sim = np.array(sim)
idx = np.argmax(sim)
print(products[idx]['title'])
print(products[idx]['description'])



