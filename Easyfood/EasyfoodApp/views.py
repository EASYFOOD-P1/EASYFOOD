from django.shortcuts import render, get_object_or_404
from EasyfoodApp.models import Product
#from product_recommendations_db import get_embedding, cosine_similarity
import numpy as np
import json
from openai import OpenAI 
from dotenv import load_dotenv, find_dotenv
import os, random

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


def home(request):
    products = Product.objects.all()
    
    #bestProd = Product.objects.get(emb="Sample title")
    prompt = request.GET.get('searchProduct')
    best_prod = None
    sim_max = -1

    if prompt:
        embedding_prompt = get_embedding(prompt)
        #embedding_prompt_adjusted = [x for elem in embedding_prompt for x in (elem, elem)]

        products = Product.objects.all()

        for product in products:
            binary_emb = product.emb
            rec_emb = list(np.frombuffer(binary_emb, dtype=np.float64))
            
            similitud = cosine_similarity(embedding_prompt, rec_emb)
            if similitud > sim_max:
                sim_max = similitud
                best_prod = product
    
    if not best_prod:

        best_prod = products[random.randint(0, len(products)-1)]

    return render(request, 'home.html', {'products': products, 'best_prod': best_prod})

def products(request):
    query = request.GET.get('searchProduct')
    results = None

    if query:
        results = Product.objects.filter(title__icontains=query)
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'results': results})

def login(request):
    return render(request, 'login.html')

def product_detail(request, product_name):

    product = get_object_or_404(Product, title=product_name)

    print(product)

    return render(request, 'product-detail.html', {'product': product})

"""
def recommendations(request):
    # CALCULAR EL EMBEDDING MAYOR DE LA BD COMPARADO CON EL PROMT Y DESPUES SELECCIONAR EL PRODUCTO QUE TENGA ESE EMBEDDING. 

    json_file_path = 'EasyfoodApp/management/commands/db.json'

    with open(json_file_path, 'r') as file:
        file_content = file.read()
        products = json.loads(file_content)
    prompt = request.GET.get('searchProduct')
    emb = get_embedding(prompt)
    sim = []
    for i in range(len(products)):
        sim.append(cosine_similarity(emb,products[i]['embedding']))
    sim = np.array(sim)
    idx = np.argmax(sim)
    bestChoiceTitle = products[idx]['title']
    bestChoiceDesc = products[idx]['description']

    return(request, 'recommendations.html', {'resultado':bestChoiceTitle})
"""
