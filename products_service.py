"""
Here be dragons!
Please ignore this section... or don't!
"""

from inspect import cleandoc
from random import choice, randint, sample


def get_category(id, categories):
    for category in categories:
        if id == category['id']:
            return category
        elif 'children' in category:
            if res := get_category(id, category['children']):
                return res
    else:
        return None


def get_products(category):
    adjectives = (
        'Animal Print',
        'Awesome',
        'Casual',
        'Formal',
        'Gorgeous',
        'Floral',
        'Simple',
        'Standard',
        'Super',
        'Stunning',
        'Unique',
    )

    # items = ('Shirt', 'T-Shirt', 'Pants', 'Dress', 'Blouse', 'Jeans', 'Trousers')
    sizes = ('XS', 'S', 'M', 'L', 'XL')
    colors = ('green', 'yellow', 'pink', 'black', 'white')

    description = cleandoc('''
        Lorem ipsum dolor sit amet, consectetur adipisicing elit.
        Numquam accusamus facere iusto,
        autem soluta amet sapiente ratione inventore nesciunt a,
        maxime quasi consectetur, rerum illum.
        ''').replace('\n', '')

    products = []

    for adj in adjectives:
        is_sale = choice((True, False, False, False))
        discount_ratio = randint(0, 75) / 100 if is_sale else 0
        stock = randint(1, 5) if is_sale else randint(0, 20)
        is_hot = not is_sale and stock > 0 and choice((True, False, False))

        products.append({
            'title': f"{adj} {category['title']}",
            'description': description * randint(1, 3),
            'long_description': ' '.join([description for i in range(10)]),
            'price': randint(1000, 9999) / 100,
            'discount_ratio': discount_ratio,
            'stock': stock,
            'sizes': sample(sizes, randint(1, len(sizes))),
            'colors': sample(colors, randint(1, len(colors))),
            'is_hot': is_hot
        })

    return products


def get_all_categories():
    return [
        {
            'id': 'men',
            'title': 'Men',
            'children': [
                {'id': 'casual', 'title': 'Casual'},
                {'id': 'sports', 'title': 'Sports'},
                {'id': 'formal', 'title': 'Formal'},
                {'id': 'standard', 'title': 'Standard'},
                {'id': 't-shirts', 'title': 'T-Shirts'},
                {'id': 'shirts', 'title': 'Shirts'},
                {'id': 'jeans', 'title': 'Jeans'},
                {'id': 'trousers', 'title': 'Trousers'},
                {
                    'id': 'other',
                    'title': 'And more…',
                    'children': [
                        {'id': 'sleep-wear', 'title': 'Sleep Wear'},
                        {'id': 'sandals', 'title': 'Sandals'},
                        {'id': 'loafers', 'title': 'Loafers'}
                    ]
                }
            ]
        },
        {
            'id': 'women',
            'title': 'Women',
            'children': [
                {'id': 'kurta-n-kurti', 'title': 'Kurta & Kurti'},
                {'id': 'trousers', 'title': 'Trousers'},
                {'id': 'casual', 'title': 'Casual'},
                {'id': 'sports', 'title': 'Sports'},
                {'id': 'formal', 'title': 'Formal'},
                {'id': 'sarees', 'title': 'Sarees'},
                {'id': 'shoes', 'title': 'Shoes'},
                {
                    'id': 'other',
                    'title': 'And more…',
                    'children': [
                        {'id': 'sleep-wear', 'title': 'Sleep Wear'},
                        {'id': 'sandals', 'title': 'Sandals'},
                        {'id': 'loafers', 'title': 'Loafers'},
                        {
                            'id': 'other',
                            'title': 'And more…',
                            'children': [
                                {'id': 'Rings', 'title': 'Rings'},
                                {'id': 'Earrings', 'title': 'Earrings'},
                                {'id': 'Jewellery Sets', 'title': 'Jewellery Sets'},
                                {'id': 'Lockets', 'title': 'Lockets'},
                                # <li class="disabled"><a class="disabled" href="#">Disabled item</a></li>
                                {'id': 'Jeans', 'title': 'Jeans'},
                                {'id': 'Polo T-Shirts', 'title': 'Polo T-Shirts'},
                                {'id': 'SKirts', 'title': 'SKirts'},
                                {'id': 'Jackets', 'title': 'Jackets'},
                                {'id': 'Tops', 'title': 'Tops'},
                                {'id': 'Make Up', 'title': 'Make Up'},
                                {'id': 'Hair Care', 'title': 'Hair Care'},
                                {'id': 'Perfumes', 'title': 'Perfumes'},
                                {'id': 'Skin Care', 'title': 'Skin Care'},
                                {'id': 'Hand Bags', 'title': 'Hand Bags'},
                                {'id': 'Single Bags', 'title': 'Single Bags'},
                                {'id': 'Travel Bags', 'title': 'Travel Bags'},
                                {'id': 'Wallets & Belts',
                                    'title': 'Wallets & Belts'},
                                {'id': 'Sunglases', 'title': 'Sunglases'},
                                {'id': 'Nail', 'title': 'Nail'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'id': 'kids',
            'title': 'Kids',
            'children': [
                {'id': 'casual', 'title': 'Casual'},
                {'id': 'sports', 'title': 'Sports'},
                {'id': 'formal', 'title': 'Formal'},
                {'id': 'standard', 'title': 'Standard'},
                {'id': 't-shirts', 'title': 'T-Shirts'},
                {'id': 'shirts', 'title': 'Shirts'},
                {'id': 'jeans', 'title': 'Jeans'},
                {'id': 'trousers', 'title': 'Trousers'},
                {
                    'id': 'other',
                    'title': 'And more…',
                    'children': [
                        {'id': 'sleep-wear', 'title': 'Sleep Wear'},
                        {'id': 'sandals', 'title': 'Sandals'},
                        {'id': 'loafers', 'title': 'Loafers'}
                    ]
                }
            ]
        },
        {'id': 'sports', 'title': 'Sports'},
        {
            'id': 'digital',
            'title': 'Digital',
            'children': [
                {'id': 'camera', 'title': 'Camera'},
                {'id': 'mobile', 'title': 'Mobile'},
                {'id': 'tablet', 'title': 'Tablet'},
                {'id': 'laptop', 'title': 'Laptop'},
                {'id': 'accesories', 'title': 'Accesories'},
            ]
        },
        {'id': 'furniture', 'title': 'Furniture'}
    ]
