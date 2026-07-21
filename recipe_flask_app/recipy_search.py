import pandas as pd


def find_recipe(name):
    recipes = pd.read_csv('recipes_sorted.csv')
    #recipy_dict = recipes.set_index('Title').T.to_dict('list')
    
    recipes = recipes.loc[recipes['Title'].str.contains(name.lower().strip())]
    recipes['Title'] = recipes['Title'].apply(str)
    recipes.sort_values('Title', axis=0, ascending=True, inplace=True, na_position='last')
    
    return recipes['Title'].values.tolist()



def sort_recipe(allergens):
    
    allergy_dict = {}
    
    for allergen in allergens:
        allergy_dict[allergen] = True
    
    recipes = pd.read_csv('recipes_sorted.csv')
    
    
    for key, value in allergy_dict.items():
        recipes = recipes.loc[recipes[key] != value]
        
    recipes['Title'] = recipes['Title'].apply(str)
    recipes.sort_values('Title', axis=0, ascending=True, inplace=True, na_position='last')
    
    return set(recipes['Title'].values.tolist())
    #return recipes['Title'].values.tolist()



def get_details(name):
    recipes = pd.read_csv('recipes_sorted.csv')
    recipy_dict = recipes.set_index('Title').T.to_dict('list')
    
    return recipy_dict[name]