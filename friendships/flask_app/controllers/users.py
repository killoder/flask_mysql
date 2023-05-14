from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.friendship import Friendship
from flask_app.models.user import User

@app.route('/users')
def ninjas():
    return render_template('user.html', friendships= Friendship.get_all())

@app.route('/create/user',methods=['POST'])
def create_user():
    User.save(request.form)
    return redirect('/friendships')