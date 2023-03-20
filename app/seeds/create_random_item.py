from faker import Faker
import random
from datetime import datetime
from app.repositories.models import OrderDetail, Order
from flask_seeder import Faker as fk

fake = Faker()

ingredients = {
    "1": {
        "name": "Tomato",
        "price": 0.90
    },
    "2": {
        "name": "Onion",
        "price": 0.99
    },
    "3": {
        "name": "Pepperoni",
        "price": 1.99
    },
    "4": {
        "name": "Chicken",
        "price": 1.50
    },
    "5": {
        "name": "Bacon",
        "price": 1.99
    },
    "6": {
        "name": "Pepper",
        "price": 0.50
    },
    "7": {
        "name": "Mushroom",
        "price": 1.99
    },
    "8": {
        "name": "Ham",
        "price": 0.99
    },
    "9": {
        "name": "Pineapple",
        "price": 0.99
    },
    "10": {
        "name": "Salami",
        "price": 2.50
    }
}

sizes = {
    "1": {
        "name": "Personal",
        "price": 1.25
    },
    "2": {
        "name": "Small",
        "price": 7.99
    },
    "3": {
        "name": "Medium",
        "price": 10.99
    },
    "4": {
        "name": "Large",
        "price": 12.99
    },
    "5": {
        "name": "Family size",
        "price": 16.99
    }
}

beverages = {
    "1": {
        "name": "Water",
        "price": 0.99
    },
    "2": {
        "name": "Coca-Cola",
        "price": 2.50
    },
    "3": {
        "name": "Beer",
        "price": 2.99
    },
    "4": {
        "name": "Lemonade",
        "price": 1.99
    },
    "5": {
        "name": "Wine",
        "price": 8.99
    }
}


def random_price_ingredient():
    return random.choices(list(ingredients.items()))

def random_price_size():
    return random.choice(list(sizes.items()))

def random_price_beverage():
    return random.choices(list(beverages.items()))


def create_random_client():
    client = {
        "client_name": fake.name(),
        "client_dni": fake.ssn(),
        "client_address": fake.address(),
        "client_phone": fake.msisdn()
    }
    return client


def create_random_ingredient():
    random_ingredient = random_price_ingredient()
    ingredients = [{
        "_id": key,
        "name": random_ingredient[str(key)]["name"],
        "price": random_ingredient[str(key)]["price"]
    } for key in random_ingredient.keys()]
    return ingredients


def create_random_size():
    random_size = random_price_size()
    key = random_size.keys()[0]
    size = {
        "_id": key,
        "name": random_size[str(key)]["name"],
        "price": random_size[str(key)]["price"]
    }
    return size


def create_random_beverage():
    random_beverage = random_price_beverage()
    beverages = [{
        "_id": key,
        "name": random_beverage[str(key)]["name"],
        "price": random_beverage[str(key)]["price"]
    } for key in random_beverage.keys()]
    return beverages


def create_clients():
    clients = []
    for i in range (10):
        clients.append(create_random_client())
    return clients


def calculate_total_price(ingredients, beverages, size):
    return sum(ingredient.price for ingredient in ingredients) + \
        sum(beverage.price for beverage in beverages) + size.price


def create_random_order(_id, clients, ingredients, beverages, size):
    client = random.choice(clients)
    order = {
        "_id": _id,
        **client,
        "date": fake.date_between(datetime.fromisoformat('2018-01-01'), datetime.fromisoformat('2023-01-01')),
        "total_price": calculate_total_price(ingredients, beverages, size),
        "size_id": size._id
    }
    return order


def list_item_maker(items, class_type):
    items_created = []
    for key, value in items.items():
        items_created.append(gen_fake_items(value["name"], class_type, value["price"], key).create()[0])
    return items_created


def gen_fake_items(item_type, item_class, price, id):
    return fk(
        cls = item_class,
        init = {
            '_id': id,
            'name': item_type,
            'price': price
        }
    )


def gen_fake_order_detail(order_detail):
    return fk(
        cls = OrderDetail, 
        init = {
            "_id": order_detail["_id"],
            "ingredient_price": order_detail["ingredient_price"],
            "order_id": order_detail["order_id"],
            "ingredient_id": order_detail["ingredient_id"], 
            "beverage_price": order_detail["beverage_price"],
            "beverage_id": order_detail["beverage_id"]
        }
    )


def gen_fake_order(order):
    return fk(
        cls = Order, 
        init = {
            "_id": order["_id"],
            "client_name": order["client_name"],
            "client_dni": order["client_dni"],
            "client_address": order["client_address"],
            "client_phone": order["client_phone"],
            "date": order["date"],
            "total_price": order["total_price"],
            "size_id": order["size_id"]
        }
    )
