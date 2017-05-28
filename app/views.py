from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
import shlex

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    form = LoginForm()
    list_of_codes = []
    if request.method == 'POST':  
        data = request.form.values()[0]

        debug = str(data)

        #TODO - cannot parse inverted commas
        list_of_codes = debug.split('\n')

        #Do machine learning magic here...


        #OUTPUT - dictionary 

        output = [
            {
                'search': 'heart attack',
                0: {
                    'code': 'A123',
                    'description': 'myocardial infarct',
                    'distance' : 0.54
                },
                1: {
                    'code': 'A122',
                    'description': 'anterior myocardial infarct',
                    'distance' : 0.32
                }   
            },
            {
                'search': 'cholera',
                0: {
                    'code': 'B123',
                    'description': 'cholera',
                    'distance' : 0.43
                },
                1: {
                    'code': 'B122',
                    'description': 'intestinal infection',
                    'distance' : 0.23
                }  
            }
        ]


    else:
        data=''
        debug = ''
        codes = []
        output = output

    return render_template(
        'index.html', 
        data=data, 
        form=form, 
        title='Synomed',
        debug=debug,
        codes=list_of_codes,
        output=output)