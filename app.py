import flask
import mysql.connector
import service

app = flask.Flask(import_name=__name__)


#
# Обработка ошибок
#
@app.errorhandler(service.errors.ValidationError)
def validation_error(error: service.errors.ValidationError):
    return flask.jsonify({
        'errors': [
            error.to_dict(),
        ]
    }), 400
# app.errorhandler


@app.errorhandler(mysql.connector.errors.OperationalError)
def validation_error(error: mysql.connector.errors.OperationalError):
    return flask.jsonify({
        'errors':
            [{
                'message': error.msg,
                'error_no': error.errno,
            }],
    }), 500
# app.errorhandler

#
# Маршруты
#
@app.post(rule='/lead.add')
def lead_add():
    serv = service.Service(app)
    response = serv.run(flask.request)

    return flask.jsonify(response), response['status']

