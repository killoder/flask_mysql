from flask import render_template, redirect, request, flash, url_for
from flask_app import app
from flask_app.models.friendship import Friendship
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect('/friendships')

@app.route('/friendships')
def friendships():
    users=User.get_all()
    friendships = Friendship.get_all()
    return render_template('index.html',users=users, friendships=friendships)

@app.route('/create/friendship', methods=['POST'])
def create_friendship():
    user_id = request.form.get('user_id')
    friend_id = request.form.get('friend_id')

    if user_id == friend_id:
        flash("You cannot add yourself as a friend!", 'friendship')
        return redirect(url_for('index'))

    friendship = Friendship.get_by_users(user_id, friend_id)
    if not friendship:
        Friendship.create(request.form)
        flash("Friendship added successfully!", 'friendship')
    else:
        flash("This friendship already exists!", 'friendship')
    return redirect('/')

@app.route('/delete/friendships/<int:id>', methods=['GET'])
def delete_friendship(id):
    friendship = Friendship.get_one({'id': id})
    if friendship:
        Friendship.delete({'id': id})
        flash("Friendship deleted successfully.", "success")
        return redirect('/')
    else:
        flash("Friendship not found.", "warning")
        return redirect('/')


