import pytest
from app.controllers import ReportController


def test_get_report(app, create_orders):
    report, error = ReportController.get_report()
    pytest.assume(error is None)
    pytest.assume(report['best_customers'])
    pytest.assume(report['most_requested_ingredient'])
    pytest.assume(report['month_with_more_revenue'])
