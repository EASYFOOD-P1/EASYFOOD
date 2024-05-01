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
   return client.embeddings.create(input = [text], model=model, dimensions=1536).data[0].embedding

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
  emb = get_embedding(products[i]['sys_description'])
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


# ESTO KJUNTO CON ALS FUNCIONES DE COSENO Y EMBEDDINGS ES LO QUE DEBE IR EN LA VISTA, ADEMAS LA PARTE EN LA QUE SE CRGA LA LAVE DE LA API Y EL CLIENTE TAMBIE NDBEN IR EN LA VISTA?
"""
req = "quiero comer algo que tenga chicken fingers y salsa pero que no sea una hamburguesa "
emb = get_embedding(req)

sim = []
for i in range(len(products)):
  sim.append(cosine_similarity(emb,products[i]['embedding']))
sim = np.array(sim)
idx = np.argmax(sim)
print(products[idx]['title'])
print(products[idx]['description'])
"""
# HACER LA VISTA RECORRIENDO EL JSON EN VEZ DE LA BD

"""
{% load static %}


<!DOCTYPE html>
<html lang="es">
    <head>

    

        <link rel="icon" href="{% static 'EasyFood/favicon.png' %}">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EasyFood - Principal</title>

        <style>
            .poppins-regular {
                font-family: "Poppins", sans-serif;
                font-weight: 500;
                font-style: normal;
            }
            header {
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            body {
                display: flex;
                flex-direction: column;
            }
            .navmenu {
                width: 50%; 
                align-items: center; 
                justify-content: right; 
                display: flex;
            }
            .logo {
                width: 50%; 
                align-items: center; 
                display: flex;
            }
            span {
                font-size: 25px;
                padding: 10px
            }
            .container {
                display: flex;
                background-color: #f0f0f0; 
                padding: 20px; 
                border-radius: 10px; 
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                justify-content: space-evenly;
                align-items: center;
                margin: 50px;
            }
            .product {
                display: none;
            }
            .showing {
                display: block;
            }
        </style>

        <!-- Bootstrap -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

        <!-- Ajax -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

        <!-- Poppins -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
    </head>
    <body>

        <div class="container">
      
          <!-- Formulario de barra de busqueda -->
          <form action="" id="form-search" method="GET">
            <div class="mb-3">
              <label for="searchProduct" class="form-label">
                Busca un Producto
              </label>
              <input type="text" id="searchProduct" class="form-control" name="searchProduct">
            </div>
            <div class="mb-3">
              <button type="submit" class="btn btn-primary">Buscar</button>
            </div>
          </form>
      
          {% if results %}
          <ul>
              {% for resultado in results %}
                  <li>{{ resultado.nombre }}</li>
              {% endfor %}
          </ul>
            {% else %}
                <p>No se encontraron resultados.</p>
            {% endif %}
          
          <div class="row row-cols-1 row-cols-md-3 g-4">
            {% for product in products %}
            <section id="seccion-{{ product.title }}">
              <div class="col">
                <div class="card">
                  <img src="{{ product.image.url }}" class="card-img-top" alt="{{ product.nombre }}">
                  <div class="card-body">
                      <h5 class="card-title">{{ product.title }}</h5>
                      <p class="card-text">{{ product.description }}</p>
                      <a href="#" class="btn btn-primary">Precio: ${{ product.price }}</a>
                  </div>
                </div>
              </div>
            </section>
            {% endfor %}
          </div>
        </div>
      
      </body>





"""
