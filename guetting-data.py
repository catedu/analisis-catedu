# Creando las estadísticas de los contenidos de CATEDU

# Importando los datos
# El número de páginas lo saco en local con el siguiente código bash:
# tree | grep -c .md$


# Recabo la información inicial de los libros:
# * Título de los libros
# * Repos
# * nº de commits
# * Si tienen o no colaboradores

import requests
import json
import time

password = getpass()
num_of_pages = 6708

r = requests.get('https://api.gitbook.com/author/catedu/books?limit=100', auth=('deleyva', password))
with open('books.json', 'w') as file:
    file.write(r.text)

with open('books.json', 'r') as infile, open('traffic.json', 'w') as outfile:
    data = json.load(infile)
    
    
    trafico_libros = {}
    counter = 0
    for libro in data['list']:
        book = {}
        traffic_url = 'https://api.gitbook.com/book/catedu/' + libro['name'] + '/traffic?period=1year'
        platforms_url = 'https://api.gitbook.com/book/catedu/' + libro['name'] + '/traffic/platforms?period=1year'
        book['title'] = str(libro['title'])º
        print(book['title'])
        book['traffic'] = requests.get(traffic_url, auth=('deleyva', password)).json()
        book['platforms'] = requests.get(platforms_url, auth=('deleyva', password)).json()
        trafico_libros[counter] = book
        counter += 1
        time.sleep(5)
    
    json.dump(trafico_libros, outfile)