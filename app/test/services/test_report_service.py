import pytest


def test_get_report_service__returns_status_200__with_orders(client, create_orders, report_uri):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    pytest.assume(response.json['best_customers'])
    pytest.assume(response.json['most_requested_ingredient'])
    pytest.assume(response.json['month_with_more_revenue'])
