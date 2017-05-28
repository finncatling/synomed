from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from app.vec_model.funcs import find_codes
import shlex

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    form = LoginForm()
    list_of_codes = []
    if request.method == 'POST':
        # data = request.form.values()

        # TODO: FIX THIS BLOODY MESS
        data = request.form
        print_data = []
        for key in data.keys():
            for value in data.getlist(key):
                print_data.append(value)
        data = print_data[0]

        debug = str(data)

        #TODO - cannot parse inverted commas
        list_of_codes = debug.split('\n')
        output = find_codes(list_of_codes)

        # output = [
        #     {
        #         'search': 'heart attack',
        #         0: {
        #             'code': 'A123',
        #             'description': 'myocardial infarct',
        #             'distance' : 0.54
        #         },
        #         1: {
        #             'code': 'A122',
        #             'description': 'anterior myocardial infarct',
        #             'distance' : 0.32
        #         }
        #     },
        #     {
        #         'search': 'cholera',
        #         0: {
        #             'code': 'B123',
        #             'description': 'cholera',
        #             'distance' : 0.43
        #         },
        #         1: {
        #             'code': 'B122',
        #             'description': 'intestinal infection',
        #             'distance' : 0.23
        #         }
        #     }
        # ]

    else:
        data = ''
        debug = ''
        list_of_codes = []
        output = dict()

    return render_template(
        'index.html', 
        data=data, 
        form=form, 
        title='Synger',
        debug=debug,
        codes=list_of_codes,
        output=output,
        # print_data=print_data
    )
