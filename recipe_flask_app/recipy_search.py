import pandas as pd
import ast


def get_recipes(name, allergens):
    
    recipes = pd.read_csv('recipes_sorted.csv')
    
    if name:
        recipes = recipes.loc[recipes['Title'].str.contains(name.lower().strip())]
        recipes['Title'] = recipes['Title'].apply(str)
        recipes.sort_values('Title', axis=0, ascending=True, inplace=True, na_position='last')
     

    allergy_dict = {}
    
    for allergen in allergens:
        allergy_dict[allergen] = True
    
    for key, value in allergy_dict.items():
        recipes = recipes.loc[recipes[key] != value]

    return recipes[['ID','Title']].set_index('ID').T.to_dict('list')




def get_details(ident):
    recipes = pd.read_csv('recipes_sorted.csv')
    
    recipes = recipes.drop(recipes.columns[5:], axis=1)
    recipes = recipes.drop(recipes.columns[0], axis=1)
    
    recipe_dict = recipes.set_index('ID').T.to_dict('list')
    recipe_list = recipe_dict[int(ident)]
    
    recipe_list[0] = recipe_list[0].title()
    recipe_list[1] = ast.literal_eval(recipe_list[1])
    #recipe_list[2].replace('/n', '<br>')
    
    
    recipe_list[2].replace('/n', ' ')

    
    return recipe_list






