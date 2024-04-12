import mysql.connector


class InsertLead:
    _mysql: mysql.connector.connection_cext.CMySQLConnection
    _lead_data: dict

    def __init__(self, mysql: mysql.connector.connection_cext.CMySQLConnection, validated_data: dict):
        self._mysql = mysql
        self._lead_data = validated_data

        # Удаление лишних данных
        self._lead_data.pop('project_settings')
    # Конструктор

    def run(self):
        # Отсеивание пустых полей
        filtered_data = {
            key: f'"{value}"' for key, value in self._lead_data.items()
            if value is not None
        }

        # Составление строки запроса
        query = (f'INSERT INTO leads ({', '.join(filtered_data.keys())}) '
                 f'VALUES ({', '.join(filtered_data.values())});')

        with self._mysql.cursor() as cursor:
            cursor.execute(query)
            self._mysql.commit()
    # run
