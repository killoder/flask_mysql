from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask import redirect, session, request, flash, render_template,url_for


@app.route('/send/message',methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    if not Message.is_valid(request.form):
        return redirect(request.referrer)
    data = {
        'sender_id' : request.form['sender_id'],
        'receiver_id' : request.form['receiver_id'],
        'message' : request.form['message']
        }
    Message.save(data)
    return redirect('/dashboard')

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/dashboard')

"""@app.route('/reply', methods=['POST'])
def reply():
    if 'user_id' not in session:
        return redirect('/')
    sender_id = request.form['sender_id']
    receiver_id = request.form['receiver_id']
    message = request.form['message']
    data = {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message
    }
    Message.save(data)
    flash('Message sent successfully')
    return redirect('/dashboard')"""

@app.route('/reply/message', methods=['POST'])
def reply_message():
    if 'user_id' not in session:
        return redirect('/')
    if not Message.is_valid(request.form):
        return redirect(request.referrer)
    data = {
        'sender_id': request.form['sender_id'],
        'receiver_id': request.form['receiver_id'],
        'message': request.form['message']
    }
    Message.save(data)
    flash('Message sent successfully!', 'successReply')
    return redirect('/dashboard')




