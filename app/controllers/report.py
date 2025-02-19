from ..repositories.managers import ReportManager


class ReportController():
    manager = ReportManager

    @classmethod
    def get_report(cls):
        try:
            return cls.manager.get_report(), None
        except Exception as e:
            return None, str(e)
