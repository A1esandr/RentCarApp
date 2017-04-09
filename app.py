from flask import Flask, url_for, request, render_template
from appmodel import AppModel
from apputils import make_rows, make_options

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    '''Загрузка основного шаблона, загрузка истории проката'''

    model = AppModel()
    if request.method == 'POST':
        if request.form['history'] == '1':
            data = model.history(request.form)
            return make_rows(data)

    template = 'index.html'
    data = {
        'bootstrap_css' : url_for('static', filename='bootstrap.min.css'),
        'jquery_js' : url_for('static', filename='jquery-3.2.0.min.js'),
        'bootstrap_js' : url_for('static', filename='bootstrap.min.js'),
        'inputmask_js' : url_for('static', filename='jquery.inputmask.bundle.min.js'),
        'main_js' : url_for('static', filename='main.js')
    }
    return render_template(template, data=data)


@app.route('/brand', methods=['GET'])
def brand():

    '''Загрузка среднего времени проката по маркам'''

    model = AppModel()
    data = model.brand_average()
    return make_rows(data)


@app.route('/place', methods=['GET'])
def place():

    '''Загрузка среднего времени проката по маршрутам'''

    model = AppModel()
    data = model.place_average()
    return make_rows(data)


@app.route('/rent', methods=['POST'])
def rent():

    '''Сохранение записи истории проката'''

    if request.method == 'POST':
        if request.form['addrent'] == '1':
            model = AppModel()
            data = model.add_rent(request.form)
            return data

    return ''


@app.route('/auto', methods=['POST'])
def auto():

    '''Добавление автомобиля'''

    if request.method == 'POST':
        if request.form['addauto'] == '1':
            model = AppModel()
            data = model.add_auto(request.form)
            return data

    return ''


@app.route('/getauto', methods=['GET'])
def get_auto():

    '''Загрузка списка автомобилей'''

    model = AppModel()
    data = model.get_auto()
    return make_options(data)


@app.route('/getplace', methods=['GET'])
def get_place():

    '''Загрузка списка пунктов взятия и возврата'''

    model = AppModel()
    data = model.get_place()
    return make_options(data)


@app.route('/getbrand', methods=['GET'])
def get_brand():

    '''Загрузка списка марок автомобилей'''

    model = AppModel()
    data = model.get_brand()
    return make_options(data)
