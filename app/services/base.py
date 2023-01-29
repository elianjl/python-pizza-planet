from flask import jsonify, request


class BaseService:
    @staticmethod
    def create(controller, request):
        entity, error = controller.create(request.json)
        response = entity if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def update(controller, request):
        entity, error = controller.update(request.json)
        response = entity if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def get_by_id(controller, request, _id):
        entity, error = controller.get_by_id(_id)
        response = entity if not error else {'error': error}
        status_code = 200 if entity else 404 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def get_all(controller, request):
        entities, error = controller.get_all()
        response = entities if not error else {'error': error}
        status_code = 200 if entities else 404 if not error else 400
        return jsonify(response), status_code