from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask import render_template, redirect, session, request, flash, abort
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/users')
def all_users():
    users = User.get_all()
    return render_template('all_users.html', users=users)

@app.route('/danger')
def danger():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return render_template('danger.html', ip_address=ip_address)


@app.route('/register',methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/dashboard')
    if not User.is_valid(request.form):
        return redirect(request.referrer)
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    User.save(data)
    return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/dashboard')
    data = {
        'email' : request.form['email']
    }
    if not User.get_user_by_email(data):
        flash('This user does not exist !','emailLogin')
        return redirect(request.referrer)
    user = User.get_user_by_email(data)
    print(user)
    if user:
        if not bcrypt.check_password_hash(user['password'], request.form['password']):
            flash('Wrong Password', 'passwordLogin')
            return redirect(request.referrer)
    session['user_id'] = user ['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    messages = Message.get_user_received_messages(data)
    user = User.get_one(data)
    message_count = User.message_count(data)
    messages = Message.get_user_received_messages(data)
    users = User.get_all()
    return render_template('dashboard.html', user=user,users=users,messages=messages,message_count=message_count)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/delete/user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.get_one({'id': user_id})
    if not user:
        return abort(404)

    User.delete_user(user_id)
    return redirect('/')



