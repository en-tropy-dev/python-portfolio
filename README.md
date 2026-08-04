# Python Portfolio

This portfolio currently consists of three items:
- churn calculation
- get transactions
- recipe flask app
  
Each of them has a dedicated folder.



### Churn calculation

**Short summary:** logistic regression model was trained to make churn predictions.

**Dataset:** project was done during python course, so the dataset was provided as part of educational program.

**Libraries:** scikit-learn, pandas



### Get transactions

**Short summary:** transactions list is being requested from handelsbanken sandbox api.

**Libraries:** requests, json, uuid, urllib

**Note:** in the beginning of the code client id is being extracted form the txt file. This file is empty in the repository, so the program will return 'there is an issue with file client_id.txt'.



### Recipe flask app

**Short summary:** it's a web app, which purpose is to search for recipes from input and filtering them out by allergens.

**Dataset:** https://github.com/josephrmartinez/recipe-dataset/tree/main

**Libraries:** flask, pandas, markupsafe, ast

**Note:** recipe dataset in folder was already sorted out by me for convenience. The original file was too big to upload. If you are interested how file was sorted, you can check sorting_recipes.py, I uploaded it in the same folder.


