import calendar

from typing import Any, List, Optional, Sequence
from sqlalchemy.sql import text, column, desc, func
from collections import Counter

from .models import Ingredient, Order, OrderDetail, Size, Beverage, db
from .serializers import (IngredientSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ma)

class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((OrderDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class ReportManager():
    session = db.session
    model_order = Order
    model_order_detail = OrderDetail
    model_ingredient = Ingredient

    @classmethod
    def get_best_customers(cls):
        clients = cls.session.query(cls.model_order.client_name, func.count(cls.model_order.client_name).label(
            'quantity')).group_by(cls.model_order.client_name).order_by(desc('quantity')).limit(3).all()
        return [{
            'client_name': client.client_name
        }
            for client in clients
        ]
    
    @classmethod
    def get_most_requested_ingredient(cls):
        ingredient_details = []
        order_detail = cls.model_order_detail.query.all()
        for ingredient_detail in order_detail:
            if ingredient_detail.ingredient_id:
                ingredient_details.append(ingredient_detail)

        ingredient_ids = [ingredient_detail.ingredient_id
                          for ingredient_detail in ingredient_details]

        if len(ingredient_ids) > 0:
            most_requested_ingredient = {
                'id': '',
                'counter': 0,
            }

            counter = Counter(ingredient_ids)

            for key in counter:
                if counter[key] > most_requested_ingredient['counter']:
                    most_requested_ingredient['counter'] = counter[key]
                    most_requested_ingredient['id'] = key

            ingredient = Ingredient.query.get(most_requested_ingredient['id'])

            return {
                'name': ingredient.name,
                'count': most_requested_ingredient['counter'],
            }
        else:
            raise Exception("Any order registered in the database")

    @classmethod
    def get_month_with_more_revenue(cls):
        month = cls.session.query(func.strftime('%m', cls.model_order.date).label('month'),
            func.sum(cls.model_order.total_price).label('total')).group_by('month').order_by(desc('total')).first()
        return {'month': calendar.month_name[int(month[0])], 'total': round(month[1], 2)}

    @classmethod
    def get_report(cls):
        return{
            "best_customers": cls.get_best_customers(),
            "most_requested_ingredient": cls.get_most_requested_ingredient(),
            "month_with_more_revenue": cls.get_month_with_more_revenue()
        }
