from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the drug data
df = pd.read_csv('Drug.csv')

# Define the recommendation functions
def recommend_drugs_for_condition(condition, num_recommendations=5):
    matching_drugs = df[df['Condition'] == condition]
    grouped_drugs = matching_drugs.groupby('Drug')[['Effective', 'EaseOfUse', 'Satisfaction']].mean()
    sorted_drugs = grouped_drugs.sort_values(by=['Effective', 'EaseOfUse', 'Satisfaction'], ascending=False)
    recommended_drugs = sorted_drugs.index.tolist()[:num_recommendations]
    return recommended_drugs

def recommend_conditions_for_drug(drug, num_recommendations=5):
    matching_conditions = df[df['Drug'] == drug]
    grouped_conditions = matching_conditions.groupby('Condition')[['Effective', 'EaseOfUse', 'Satisfaction']].mean()
    sorted_conditions = grouped_conditions.sort_values(by=['Effective', 'EaseOfUse', 'Satisfaction'], ascending=False)
    recommended_conditions = sorted_conditions.index.tolist()[:num_recommendations]
    return recommended_conditions

# Define the app routes
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/TSA')
def TSA():
    return render_template('TSA.html')

@app.route('/Sentiment')
def Sentiment():
    return render_template('Sentiment.html')

@app.route('/Recommend')
def recommend():
    return render_template('recommendation.html')

@app.route('/search')
def search():
    return render_template('searchengine.html')

@app.route('/recommend-condition')
def recommend_condition():
    condition = request.args.get('condition')
    if not condition:
        return 'Error: Please enter a medical condition.'
    recommended_drugs = recommend_drugs_for_condition(condition, num_recommendations=5)
    return render_template('results.html', title='Recommended Drugs for {}'.format(condition), recommendations=recommended_drugs)

@app.route('/recommend-drug')
def recommend_drug():
    drug = request.args.get('drug')
    if not drug:
        return 'Error: Please enter a drug name.'
    recommended_conditions = recommend_conditions_for_drug(drug, num_recommendations=5)
    return render_template('results.html', title='Recommended Conditions for {}'.format(drug), recommendations=recommended_conditions)

if __name__ == '__main__':
    app.run(debug=True)
