from flask import Flask, request, render_template, url_for
from markupsafe import escape
from recipy_search import get_recipes, get_details


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        dish_name = escape(request.form['dish name'])
        allergens = request.form.getlist('checkbox')
        
        dish_dict = get_recipes(dish_name, allergens)
        
        if dish_dict:
            return render_template('recipe_list.html', dish_dict=dish_dict, dish_num=len(dish_dict))
        
        else:
            return "I'm sorry, it seems we were not able to find anything"
    return render_template('main.html')



@app.route('/<dish_id>', methods=['GET', 'POST'])
def display(dish_id):
    if request.method == 'GET':
        dish_details = get_details(dish_id)
        return render_template('recipe.html',dish_details=dish_details)


if __name__ == '__main__':
    app.run(debug=True)