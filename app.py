from flask import Flask, render_template, g, request, abort
from os import environ  # , listdir, path
from pathlib import Path
import locale
import sqlite3


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
        # If `row_factory` is not set, retrieval methods return tuples,
        # and you have to use indices instead of named columns.
        conn.row_factory = sqlite3.Row
        # Alternatively, you can set your own factory function.
        # conn.row_factory = lambda cur, row: dict((cur.description[idx][0], value) for idx, value in enumerate(row))
        g.conn = conn       # setattr(g, 'conn', conn)

    return g.conn


""" @app.before_request
def open_connection():
    '''
    Executes before * every * request
    '''
    g.conn = sqlite3.connect(DATABASE_PATH)
    g.conn.row_factory = sqlite3.Row """


@app.before_request
def get_categories():
    '''
    Executes before *every* request, beacuse categories are needed for menu.
    `g` is a global object to store stuff for a *single* request
    '''

    # Quick return if request comes from a static asset
    if not request or request.endpoint == 'static':
        return

    # Quick return if categories are already in `g`
    if hasattr(g, 'categories'):
        return

    cursor = get_conn().cursor()

    categories = cursor.execute(
        '''
        SELECT id, title, parent, other
        FROM category
        ORDER BY parent, title
        '''
    ).fetchall()

    cursor.close()

    setattr(g, 'categories', categories)    # g.categories = categories


@app.route('/')
def home():
    cursor = get_conn().cursor()

    men_random_products = cursor.execute(
        '''
        SELECT pr.id, pr.title, pr.description, pr.price, pr.discount_ratio, pr.stock, pr.is_hot, pr.category_id
        FROM product pr
        INNER JOIN category ca ON pr.category_id = ca.id
        WHERE ca.parent = 'Men'
        ORDER BY RANDOM() LIMIT 8
        '''
    ).fetchall()

    women_random_products = cursor.execute(
        '''
        SELECT pr.id, pr.title, pr.description, pr.price, pr.discount_ratio, pr.stock, pr.is_hot, pr.category_id
        FROM product pr
        INNER JOIN category ca ON pr.category_id = ca.id
        WHERE ca.parent = 'Women'
        ORDER BY RANDOM() LIMIT 8
        '''
    ).fetchall()

    sports_random_products = cursor.execute(
        '''
        SELECT pr.id, pr.title, pr.description, pr.price, pr.discount_ratio, pr.stock, pr.is_hot, pr.category_id
        FROM product pr
        INNER JOIN category ca ON pr.category_id = ca.id
        WHERE ca.title = 'Sports'
        ORDER BY RANDOM() LIMIT 8
        '''
    ).fetchall()

    cursor.close()

    return render_template(
        'home.html',
        men_products=men_random_products,
        women_products=women_random_products,
        sports_products=sports_random_products
    )


@app.route('/products/<category_id>')
def product_list(category_id):
    cursor = get_conn().cursor()

    category = cursor.execute(
        '''
        SELECT title, parent
        FROM category
        WHERE id = ?
        ''',
        (category_id,)
    ).fetchone()

    if category is None:
        abort(404)

    products = cursor.execute(
        '''
        SELECT id, title, description, price, discount_ratio, stock, is_hot, category_id
        FROM product
        WHERE category_id = ?
        ORDER BY title
        ''',
        (category_id,)
    ).fetchall()

    cursor.close()

    # app.logger.debug(category)
    # app.logger.debug(products)

    return render_template('products/list.html', category=category, products=products)


@app.route('/products/<category_id>/<product_id>')
def product_details(category_id, product_id):
    cursor = get_conn().cursor()

    category = cursor.execute(
        '''
        SELECT title
        FROM category
        WHERE id = ?
        ''',
        (category_id,)
    ).fetchone()

    if category is None:
        abort(404)

    product = cursor.execute(
        '''
        SELECT id, title, description, price, discount_ratio, stock, is_hot
        FROM product
        WHERE id = ?
        ''',
        (product_id,)
    ).fetchone()

    if product is None:
        abort(404)

    cursor.close()

    # app.logger.debug(category)
    # app.logger.debug(product)

    return render_template('products/details.html', category=category, product=product)


""" @app.teardown_request
def close_connection(ctx):
    '''
    Close connection on request teardown
     '''
    if hasattr(g, 'conn'):
        app.logger.debug('» Teardown Request')
        app.logger.debug('» Connection closed')
        g.conn.close() """


@app.teardown_appcontext
def close_connection(err):
    '''
    Close the connection to the DB.
    The `teardown_appcontext` decorator with ensure
    that this function gets called at the end of each request,
    even when an exception is raised.
    '''
    if conn := g.pop('conn', None):
        app.logger.debug('» Teardown AppContext')
        app.logger.debug('» Connection closed')
        conn.close()

    if err is not None:
        app.logger.error(err)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.debug(e)
    return render_template('errors/404.html'), 404


@app.template_filter('currency')
def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'el_GR')
    return locale.currency(value, symbol=True, grouping=True)


@app.cli.command('init-db')
# @click.argument('init-db')
def init_db():
    '''
    A CLI command to create the DB, running `flask init-db`,
    by executing the scripts in the "migrations" folder
    '''
    migrations_path = Path(__file__).parent / '_migrations'
    for migration in migrations_path.glob('*.sql'):
        with app.app_context():
            with get_conn() as conn:
                with app.open_resource(migration, mode='r') as f:
                    conn.executescript(f.read())

    """ migrations_path = path.join(BASE_PATH, '_migrations')
    for file in listdir(migrations_path):
        file_path = path.join(migrations_path, file)
        with app.app_context():
            with get_conn() as con:
                with app.open_resource(file_path, mode='r') as f:
                    contents = f.read()
                    con.cursor().executescript(contents) """


if __name__ == '__main__':
    app.run(host='localhost', port=environ.get('SERVER_PORT', 5000), debug=True)
