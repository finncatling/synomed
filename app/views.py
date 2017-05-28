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


    else:
        data=''
        debug = ''
        codes = []

    return render_template(
        'index.html', 
        data=data, 
        form=form, 
        title='Synomed',
        debug=debug,
        codes=list_of_codes)