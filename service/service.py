import typing
import configparser
import flask
import mysql.connector
import service.commands


class Service:
    _app: flask.Flask
    _mysql: mysql.connector.connection_cext.CMySQLConnection

    def __init__(self, app: flask.Flask):
        # Подключение приложения
        self._app = app

        # Подключение к базе данных
        config = configparser.ConfigParser()
        config.read('config.ini')

        self._mysql = mysql.connector.connect(
                host=config.get(section='DATABASE', option='host'),
                database=config.get(section='DATABASE', option='database'),
                user=config.get(section='DATABASE', option='user'),
                password=config.get(section='DATABASE', option='password'),
        )
    # Конструктор

    def __del__(self):
        self._mysql.close()
    # Деструктор

    def run(self, request: flask.Request) -> dict[str, typing.Any]:
        # Валидация
        validated_data = service.commands.Validate(self._mysql).run(request)

        # Определение источника
        validated_data['source'] = service.commands.GetSource(validated_data).run()

        # Проверка проекта
        if validated_data['project_settings']['enabled'] is False:
            return {
                'status': 200,
                'message': 'Проект отключен',
            }

        # Добавление данных в БД
        service.commands.InsertLead(mysql=self._mysql, validated_data=validated_data).run()

        return {
            'status': 201,
            'message': 'OK',
        }
    # run