from flask import Flask, request, render_template, url_for
from recipy_search import find_recipe, sort_recipe, get_details

app = Flask(__name__)

@app.route('/')
def welcome():
    return "Hello there!"

@app.route('/recipe', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        dish_name = request.form['dish name']
        dish_list = find_recipe(dish_name)
        dish_str = ''
        if dish_list:
            for dish in dish_list:
                dish_str += f'<button name="{dish}" onclick="display({dish})">{dish}</button><br>'
            #dish_str = '<br>'.join(dish_list) 
            return dish_str
        else:
            return "I'm sorry, it seems we were not able to find anything"
    return render_template('recipe.html')


@app.route('/allergen', methods=['GET', 'POST'])
def filters():
    if request.method == 'POST':
        allergens = request.form.getlist('checkbox')
        recipe_list = sort_recipe(allergens)
        if recipe_list:
            recipe_str = ''
            for recipe in recipe_list:
                recipe_str += f'<button name="{recipe}" onclick="display({recipe})">{recipe}</button><br>'
            #recipe_str = '<br>'.join(recipe_list)
            return recipe_str
        else:
            return "I'm sorry, it seems we were not able to find anything"
    return render_template('allergens.html')


@app.route('/<dish_name>')
def display(dish_name):
    dish_details = get_details(dish_name)
    return dish_details


if __name__ == '__main__':
    app.run(debug=True)