from flask_seeder import Seeder
from random import choice, choices
from app.seeds.create_random_item import *
from app.repositories.models import *

class DatabaseSeeder(Seeder):
    def run(self):
        sizes_created = list_item_maker(sizes, Size)
        ingredients_created = list_item_maker(ingredients, Ingredient)
        beverages_created = list_item_maker(beverages, Beverage)
        
        self.save(sizes_created)
        self.save(ingredients_created)
        self.save(beverages_created)
        
        created_orders = []
        order_detail = []
        order_detail_counter = 0
        clients = create_clients()

        for order_number in range(1, 101):
            random_ingredients = choices(ingredients_created)
            random_beverages = choices(beverages_created)
            random_size = choice(sizes_created)

            random_order = create_random_order(order_number, clients, random_ingredients, random_beverages, random_size)

            for ingredient in random_ingredients:
                order_detail_counter += 1
                ingredient_detail = {
                    "_id": order_detail_counter,
                    "ingredient_price": ingredient.price,
                    "order_id": order_number,
                    "ingredient_id": ingredient._id, 
                    "beverage_price": None,
                    "beverage_id": None
                }
                order_detail.append(gen_fake_order_detail(ingredient_detail).create()[0])

            for beverage in random_beverages:
                order_detail_counter += 1
                beverage_detail = {
                    "_id": order_detail_counter,
                    "ingredient_price": None,
                    "order_id": order_number,
                    "ingredient_id": None, 
                    "beverage_price": beverage.price,
                    "beverage_id": beverage._id
                }
                order_detail.append(gen_fake_order_detail(beverage_detail).create()[0])
            
            self.save(order_detail)
            order_detail.clear()
            created_orders.append(gen_fake_order(random_order).create()[0])

        self.save(created_orders)


    def save(self, data: list):
        for item in data:
            self.db.session.add(item)
