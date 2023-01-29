from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from .base import BaseService
from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
def create_beverage():
    return BaseService.create(BeverageController, request)


@beverage.route('/', methods=PUT)
def update_beverage():
    return BaseService.update(BeverageController, request)


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return BaseService.get_by_id(BeverageController, request, _id)


@beverage.route('/', methods=GET)
def get_beverages():
    return BaseService.get_all(BeverageController, request)
