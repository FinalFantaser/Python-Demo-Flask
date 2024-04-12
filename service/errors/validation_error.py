import typing


class ValidationError(Exception):
    STATUS_CODE = 400

    def __init__(self, message, data=None):
        self._message = message
        self._data = data
    # Конструктор

    def to_dict(self):
        result = {'message': self._message}

        if self._data is not None:
            result['data'] = self._data

        return result
    # to_dict
