from flask_app import app
from flask_app.models.email import Email
from flask import render_template, redirect, session, request, flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
    if not Email.is_valid(request.form):
        return redirect('/')
    flash('Success! The email address you entered is VALID ! Thank you !')
    Email.save(request.form)
    return redirect('/results')

@app.route('/results')
def results():
    return render_template("results.html",emails=Email.get_all())

@app.route('/destroy/<int:id>')
def destroy_email(id):
    data = {
        "email_id": id
    }
    Email.destroy(data)
    return redirect('/results')