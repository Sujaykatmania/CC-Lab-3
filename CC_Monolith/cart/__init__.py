import json
from products import Product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])

    def add_product(self, product: Product):
        self.contents.append(product)
        self.cost += product.price

    def remove_product(self, product: Product):
        self.contents.remove(product)
        self.cost -= product.price


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    items = []
    for cart_detail in cart_details:
        contents = cart_detail['contents']
        try:
            evaluated_contents = json.loads(contents)
        except json.JSONDecodeError:
            continue  # Skip invalid entries
        items.extend(evaluated_contents)

    # Optimized batch retrieval of products
    products_list = products.get_products(items)
    return [product for product in products_list if product is not None]


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
