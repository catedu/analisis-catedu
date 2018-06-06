import json
import requests

r = requests.get('https://api.gitbook.com/author/catedu/books')
with open('data.json', 'w') as file:
    file.write(r.text)