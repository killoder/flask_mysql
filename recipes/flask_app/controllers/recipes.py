from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import redirect, session, request, render_template

@app.route('/add/recipe')
def addRecipe():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('addRecipe.html', loggedUser = user)
    return redirect('/')

@app.route('/create/recipe', methods = ['POST'])
def createRecipe():
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data1)
        data ={
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'dateMade': request.form.get('dateMade', ''),
            'under30': request.form.get('under30', ''),
            'user_id': session['user_id']
        }
        if not Recipe.validate_recipe(data):
            return redirect(request.referrer)
        Recipe.save(data)
        return redirect('/')
    return redirect('/')

@app.route('/delete/recipe/<int:id>')
def deleteRecipe(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'recipe_id': id
        }
        user = User.get_user_by_id(data)
        recipe = Recipe.get_recipe_by_id(data)
        if user['id'] == recipe['user_id']:
            Recipe.delete(data)
            return redirect('/')
        return redirect(request.referrer)
    return redirect('/')

@app.route('/view/recipe/<int:id>')
def viewRecipe(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'recipe_id': id
        }
        user = User.get_user_by_id(data)
        recipe = Recipe.get_recipe_by_id(data)
        return render_template('viewRecipe.html', loggedUser =user, recipe = recipe)
    return redirect('/')

@app.route('/edit/recipe/<int:id>')
def editRecipe(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'recipe_id': id
        }
        user = User.get_user_by_id(data)
        recipe = Recipe.get_recipe_by_id(data)
        if user['id'] == recipe['user_id']:
            return render_template('editRecipe.html', loggedUser =user, recipe = recipe)
        return redirect('/')
    return redirect('/')

@app.route('/update/recipe/<int:id>', methods = ['POST'])
def updateRecipe(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'recipe_id': id
        }
        user = User.get_user_by_id(data1)
        recipe = Recipe.get_recipe_by_id(data1)

        data ={
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'dateMade': request.form.get('dateMade', ''),
            'under30': request.form.get('under30', ''),
            'recipe_id': id
        }
        if not Recipe.validate_recipe(data):
            return redirect(request.referrer)
        if user['id'] == recipe['user_id']:

            Recipe.update(data)
            return redirect('/')
        return redirect('/')
    return redirect('/')