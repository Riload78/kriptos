from cripto import app
from flask import render_template
from cripto.model.movement import MovementDAO

##config = app.config
dao = MovementDAO(app.config.get('PATH_SQLITE', 'valor_por_defecto'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/v1/all')
def get_all():
    movements = dao.get_all()
    return 'HOLA API'