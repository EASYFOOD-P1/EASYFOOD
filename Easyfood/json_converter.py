import json


json_file_path = 'EasyfoodApp/management/jsonMYSQLDBEasyfood.json'

with open(json_file_path, 'r') as file:
    file_content = file.read()
    old_products = json.loads(file_content)

new_products = []

for old_product in old_products:
    if old_product["imagen_producto"] != "data:image/gif,base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7":
        product = {
            "title": old_product["nombre_producto"],
            "description": old_product["descripcion_producto"],
            "price": old_product["precio_producto"],
            "image": old_product["imagen_producto"]
        }
        new_products.append(product)



with open('EasyfoodApp/management/commands/db.json', 'w') as json_file:
    json.dump(new_products, json_file, indent=4)  # The 'indent' parameter is optional for pretty formatting

print(f"Data saved to db.json")