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
    random_ingredient = random.choice(list(ingredients.keys()))
    return random_ingredient, ingredients[random_ingredient]

def random_price_size():
    random_size = random.choice(list(sizes.keys()))
    return random_size, sizes[random_size]

def random_price_beverage():
    random_beverage = random.choice(list(beverages.keys()))
    return random_beverage, beverages[random_beverage]


def create_random_customer():
    customer = {
        "client_name": fake.name(),
        "client_dni": fake.ssn(),
        "client_address": fake.address(),
        "client_phone": fake.msisdn()
    }
    return customer

customers = []
for i in range (10):
    customers.append(create_random_customer())


def create_random_ingredient():
    ingredient = {
        "name": random_price_ingredient()[0], 
        "price": random_price_ingredient()[1]
    }
    return ingredient

def create_random_size():
    size = {
        "name": random_price_size()[0], 
        "price": random_price_size()[1]
    }
    return size

def create_random_beverage():
    beverage = {
        "name": random_price_beverage()[0], 
        "price": random_price_beverage()[1]
    }
    return beverage
