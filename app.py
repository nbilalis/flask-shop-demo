from flask import Flask, render_template
from os import environ

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'home.html',
        men_products=get_all_products(8),
        women_products=get_all_products(8),
        sports_products=get_all_products(8)
    )




@app.template_filter('currency')
def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'el_GR')
    return locale.currency(value, symbol=True, grouping=True)


if __name__ == '__main__':
    app.run(host='localhost', port=environ.get('SERVER_PORT', 5000), debug=True)
