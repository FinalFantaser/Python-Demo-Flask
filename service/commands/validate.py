import re
import json
import flask
import mysql.connector
import service.errors


class Validate:
    _mysql: mysql.connector.connection_cext.CMySQLConnection
    _project_id: int
    _host: str
    _settings: dict

    def __init__(self, mysql: mysql.connector.connection_cext.CMySQLConnection):
        self._mysql = mysql
    # Конструктор

    def run(self, request: flask.Request):
        body = request.get_json(silent=True)

        # Запрос не должен быть пустым
        if body is None:
            raise service.errors.ValidationError(message='Тело запроса пустое')

        # Проверка обязательных полей
        if 'api_token' not in body:
            raise service.errors.ValidationError(message='Отсутствует поле api_token')

        if 'host' not in body:
            raise service.errors.ValidationError(message='Отсутствует поле host')

        if 'phone' not in body:
            raise service.errors.ValidationError(message='Отсутствует поле phone')

        # Проверка phone
        if re.match(pattern='^7\d{10}$', string=body['phone']) is None:
            raise service.errors.ValidationError(message='Некорректный формат phone', data={'lead': body})

        # Проверка достоверности api_token
        with self._mysql.cursor() as cursor:
            cursor.execute(f'SELECT id, settings from projects where api_token="{body['api_token']}"')
            result = cursor.fetchall()
            if len(result) < 1:
                raise service.errors.ValidationError(message="Неправильный токен проекта", data={'lead': body})
            self._settings = json.loads(result[0][1])
            self._project_id = result[0][0]

        # Проверка достоверности host
        with self._mysql.cursor() as cursor:
            cursor.execute(f'SELECT host from hosts where project_id={self._project_id} AND host="{body['host']}"')
            result = cursor.fetchall()
            if len(result) < 1:
                raise service.errors.ValidationError(message="Неправильный хост проекта", data={'lead': body})
            self._host = result[0][0]

        return {
            'project_id': self._project_id,
            'project_settings': self._settings,
            'host': self._host,
            'phone': body['phone'],
            'surname': body['surname'] if 'surname' in body else None,
            'name': body['name'] if 'name' in body else None,
            'patronymic': body['patronymic'] if 'patronymic' in body else None,
            'email': body['email'] if 'email' in body else None,
            'manual_city': body['city'] if 'city' in body else None,
            'cost': body['cost'] if 'cost' in body else None,
            'comment': body['comment'] if 'comment' in body else None,
            'owner': 'API',

            'utm_source': body['comment'] if 'comment' in body else None,
            'utm_medium': body['utm_medium'] if 'utm_medium' in body else None,
            'utm_campaign': body['utm_campaign'] if 'utm_campaign' in body else None,
            'utm_content': body['utm_content'] if 'utm_content' in body else None,
            'utm_term': body['utm_term'] if 'utm_term' in body else None,

            'ip': request.remote_addr,
            'referrer': request.referrer,
            'url_query_string': request.query_string.decode('utf-8'),
        }
    # validate
