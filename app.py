from flask import Flask, render_template, g, request, abort
from os import environ  # , listdir, path
from pathlib import Path
import locale
import sqlite3

from products_service import get_product, get_all_products, get_category, get_all_categories

app = Flask(__name__)

# Get the Database path with the help of the `os.path` module.
# BASE_PATH = path.dirname(path.abspath(__file__))
# DATABASE_PATH = path.join(BASE_PATH, 'data/flask-news.db')

# Get the Database path with the help of the `pathlib.Path` module
# The `/` operator is overloaded and essentially perfmors a join.
DATABASE_PATH = Path(__file__).parent / 'data/flask-shop.db'


def get_conn():
    '''
    Get a connection to the database.
    First, check if the connection is already open and stored in the `g` object.
    If not, create a new connection and store there.
    '''
    if 'conn' not in g:     # hasattr(g, 'conn')
        # app.logger.debug(f"» New Connection requested from endpoint '{request.endpoint}'")
        conn = sqlite3.connect(DATABASE_PATH)
        # If `row_factory` is not set, retrieval methods return tuples.
        conn.row_factory = sqlite3.Row
        g.conn = conn       # setattr(g, 'conn', conn)

    return g.conn


""" @app.before_request
def open_connection():
    '''
    Executes before * every * request
    '''
    g.conn = sqlite3.connect(DATABASE_PATH)
    g.conn.row_factory = sqlite3.Row """


@app.route('/')
def home():
    categories = get_all_categories()

    return render_template(
        'home.html',
        men_category=get_category('men', categories),
        women_category=get_category('women', categories),
        sports_category=get_category('sports', categories),
        men_products=get_all_products(8),
        women_products=get_all_products(8),
        sports_products=get_all_products(8)
    )


@app.route('/products/<category_id>')
def product_list(category_id):
    category = get_category(category_id, get_all_categories())
    products = get_all_products()

    app.logger.debug(category)
    app.logger.debug(products)

    return render_template('products/list.html', category=category, products=products)


@app.route('/products/<category_id>/<product_id>')
def product_details(category_id, product_id):
    category = get_category(category_id, get_all_categories())
    product = get_product(product_id)

    app.logger.debug(category)
    app.logger.debug(product)

    return render_template('products/details.html', category=category, product=product)


@app.route('/products/<product_id>/api')
def get_product_json(product_id):
    return get_product(product_id)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.debug(e)
    return render_template('errors/404.html'), 404


@app.before_request
def store_stuff_in_g():
    """
    Executes before *every* request
    g is a global object to store stuff for a *single* request
    """
    g.products = get_all_products()
    g.categories = get_all_categories()


@app.template_filter('currency')
def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'el_GR')
    return locale.currency(value, symbol=True, grouping=True)


if __name__ == '__main__':
    app.run(host='localhost', port=environ.get('SERVER_PORT', 5000), debug=True)
