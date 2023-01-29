from faker import Faker
import random
fake = Faker()

ingredients = {
    "Tomato": 0.99,
    "Onion": 0.99,
    "Pepperoni": 1.99,
    "Chicken": 1.50,
    "Bacon": 1.99,
    "Pepper": 0.50,
    "Mushroom": 1.99,
    "Ham": 0.99,
    "Pineapple": 0.99,
    "Salami": 2.50
}

sizes = {
    "Personal": 1.25,
    "Small": 7.99,
    "Medium": 10.99,
    "Large": 12.99,
    "Family size": 16.99
}

beverages = {
    "Water": 0.99,
    "Coca-Cola": 2.50,
    "Beer": 2.99,
    "Lemonade": 1.99,
    "Wine": 8.99
}


def random_price_ingredient():
    return random.choice(list(ingredients.items()))

def random_price_size():
    return random.choice(list(sizes.items()))

def random_price_beverage():
    return random.choice(list(beverages.items()))


def create_random_client():
    client = {
        "client_name": fake.name(),
        "client_dni": fake.ssn(),
        "client_address": fake.address(),
        "client_phone": fake.msisdn()
    }
    return client

clients = []
for i in range (10):
    clients.append(create_random_client())


def create_random_ingredient():
    ingredient = random_price_ingredient()
    ingredient = {
        "name": ingredient[0],
        "price": ingredient[1]
    }
    return ingredient

def create_random_size():
    size = random_price_size()
    size = {
        "name": size[0],
        "price": size[1]
    }
    return size

def create_random_beverage():
    beverage = random_price_beverage()
    beverage = {
        "name": beverage[0],
        "price": beverage[1]
    }
    return beverage


def fill_database():
    return None


def create_random_order():
    client = random.choice(clients)

    new_order = {
        "client_name": client["client_name"],
        "client_dni": client["client_dni"],
        "client_address": client["client_address"],
        "client_phone": client["client_phone"],
    }
    return new_order