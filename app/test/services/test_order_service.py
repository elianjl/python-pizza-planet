import pytest
import json
import random


def test_get_order_by_id_service(client, order_uri, create_orders):
    random_order = random.choice(create_orders)
    current_order = json.loads(random_order.data)
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)


def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_orders = {order['_id']: order for order in response.json}
    for order in create_orders:
        pytest.assume(json.loads(order.data)['_id'] in returned_orders)