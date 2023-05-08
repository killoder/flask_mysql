from flask_app import app
from flask_app.models.dojo import Dojo
from flask import render_template, redirect, request, session, flash, url_for


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if Dojo.is_valid(request.form):
        Dojo.save(request.form)
        return redirect('/display_result')
    return redirect('/')

@app.route('/display_result')
def display_result():
    return render_template('result.html', dojo = Dojo.get_last_dojo())



'''
@app.route('/register', methods=['POST'])
def register():
    if not Dojo.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # ... do other things
    return redirect('/dashboard')


@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "username": request.form['username'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = Dojo.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = Dojo.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")


@app.route('/update/<int:id>', methods= ['POST'])
def updateUserInDb(id):
    data = {
        'user_id': id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    User.update(data)
    return redirect('/')


@app.route('/user/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Dojo.destroy(data)
    return redirect(request.referrer)

'''
