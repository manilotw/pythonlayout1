from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
from collections import defaultdict

wines_excel = pd.read_excel('wine3.xlsx', sheet_name='Лист1')
wines = wines_excel.to_dict(orient='records')

wine_categories = defaultdict(list)

for wine in wines:
    wine_categories[wine['Категория']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')
wine_age = datetime.datetime.now().year - 1920


def get_year_word(number):
    last_digit = number % 10
    last_two_digits = number % 100

    if 11 <= last_two_digits <= 20:
        word = "лет"
    elif last_digit == 1:
        word = "год"
    elif last_digit in (2, 3, 4):
        word = "года"
    else:
        word = "лет"

    return word


rendered_page = template.render(
    wine_age=f'Уже {wine_age} {get_year_word(wine_age)} с вами',
    wines_type=dict(wine_categories)
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
