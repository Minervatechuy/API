from flask import Flask, jsonify, render_template, request, json
from flask_cors import CORS  # Para que se permita la política CORS
import mariadb
import configDB as configDB

app = Flask(__name__)
# Para aumentar el tamaño máximo de mensaje de solicitud
app.config['MAX_CONTENT_LENGTH'] = 35 * 1000 * 1000
CORS(app)  # Aplica la política de CORS sobre esta aplicación

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'Autor': 'MinervaTech',
                    'Nombre': 'API Simulador',
                    'Descripcion': 'API Simulador'}
                    )

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    conexion = configDB.connect()
    cur = conexion.cursor()
    sql= "SELECT * FROM usuarios"
    cur.execute (sql)
    myresult = cur.fetchall()
    return "{}".format(myresult)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

