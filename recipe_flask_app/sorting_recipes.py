import pandas as pd

allergy_dict = {"milk":
                ["milk","cheese","yogurt","butter","kefir","sour cream","cheddar","mozzarella","parmesan","heavy cream","ice cream","pecorino romano", "provolone","ricotta","parmigiano","gorgonzola","taleggio","queso fresco"], 
                "eggs": ["egg", "yolk"], 
                "fish": ["anchovy","bass","catfish","cod","fish","flounder","grouper","haddock","hake","halibut","herring","mahi","perch","pike","pollock","salmon","shark","snapper","sole","swordfish","tilapia","trout","tuna","walleye"], 
                "shellfish":["abalone","clam","conch","crab","crawfish","cuttlefish","limpet","lobster","mollusk","mussel","octopus","oyster","scallop","sea cucumber","sea urchin","shellfish","shrimp","squid","whelk","winkle"], 
                "tree nuts": ["almond","brazil nut","bush nut","cashew","ginko nut","hazelnut","hickory nut","lichee nut","macadamia nut","nangai nut","pecan","pine nut","pistachio","shea nut","walnut"], 
                "peanuts": ["peanut"], 
                "wheat": ["wheat", "flour","bread","loaf","croissant"], 
                "soybeans": ["soy"], 
                "sesame": ["sesame","sesame oil","sesame seeds"]}

recipes = pd.read_csv('recipes.csv')
recipes.dropna()
recipes = recipes.drop(recipes.columns[0], axis=1)
recipes = recipes.drop('Image_Name', axis=1)
recipes = recipes.drop('Cleaned_Ingredients', axis=1)
recipes['Ingredients'] = recipes['Ingredients'].str.lower()
recipes['Title'] = recipes['Title'].str.lower()

print(recipes.head())

for key, value in allergy_dict.items():
    for item in value:
        recipes.loc[recipes['Ingredients'].str.contains(item), key] = True
    
    recipes[key] = recipes[key].fillna(False)
    
recipes.insert(0, 'ID', range(1, 1 + len(recipes)))
recipes.to_csv('recipes_sorted.csv')

print(recipes.head())