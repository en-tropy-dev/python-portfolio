from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pandas as pd


def calc_data():

    customer_data = pd.read_csv('customer_data.csv')
    print(customer_data.head())

    customer_data['tenure'] = customer_data['tenure'].fillna(customer_data['tenure'].median(numeric_only = True))
    
    state_encoder = LabelEncoder()
    customer_data['encoded_state'] = state_encoder.fit_transform(customer_data['state'])
    
    scaler = StandardScaler()
    customer_data[['tenure', 'monthly_charges']] = scaler.fit_transform(customer_data[['tenure', 'monthly_charges']])

    print(customer_data.head())

    
    x = customer_data[['tenure', 'monthly_charges', 'encoded_state']]
    y = customer_data['churn']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred)}")

    churn_probabilities = model.predict_proba(x_test)[:, 1]
    avg_churn_prob = churn_probabilities.mean()
    high_risk_customers = 0

    for y in churn_probabilities:
        if y > avg_churn_prob:
            high_risk_customers += 1

    churn_rate_by_state = []
    high_risk_by_state = []


    for state, group in customer_data.groupby('state'):
        churn_rate, high_risk_count = calculate_churn_and_high_risk(group['churn'], avg_churn_prob)
        churn_rate_by_state.append({'state': state, 'churn_rate': churn_rate})
        high_risk_by_state.append({'state': state, 'high_risk': high_risk_count})

    churn_rate_by_state_df = pd.DataFrame(churn_rate_by_state)
    high_risk_by_state_df = pd.DataFrame(high_risk_by_state)

    print("Results of your analysis for reference:")
    print(f"Average Churn Probability: {avg_churn_prob}")
    print(f"High-Risk Customers: {high_risk_customers}")
    print(f"Churn Rate by State:\n {churn_rate_by_state_df}")
    print(f"High-Risk Customers by State:\n {high_risk_by_state_df}")

    with open('churn_results.txt', 'w') as f:
        f.write(f"Average Churn Probability: {avg_churn_prob}\n\n")
        f.write(f"High-Risk Customers: {high_risk_customers}\n\n")
        f.write(f"Churn Rate by State:\n {churn_rate_by_state_df}\n\n")
        f.write(f"High-Risk Customers by State:\n {high_risk_by_state_df}")

    return avg_churn_prob, high_risk_customers, churn_rate_by_state_df, high_risk_by_state_df

def calculate_churn_and_high_risk(churn_series, avg_churn_prob):

    churn_rate = churn_series.sum()/len(churn_series)
    high_risk_mask = (churn_series > avg_churn_prob)
    high_risk_count = high_risk_mask.sum()
    return churn_rate, high_risk_count

calc_data()