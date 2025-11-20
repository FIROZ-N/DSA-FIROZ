from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV
df = pd.read_csv('VotingFinal.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    countries = df['Country'].unique()
    result = None
    selected_country = None

    if request.method == 'POST':
        selected_country = request.form['country']
        # Filter rows where the selected country received points
        filtered = df[df['Country'] == selected_country]
        # Group by Giver and sum the scores
        points_by_country = filtered.groupby('Giver')['Score'].sum()
        if not points_by_country.empty:
            max_giver = points_by_country.idxmax()
            max_score = points_by_country.max()
            result = f"The country that has given the most points to {selected_country} is {max_giver} with {max_score} points!"
        else:
            result = f"No voting data available for {selected_country}."

    return render_template('index.html', countries=countries, result=result, selected_country=selected_country)

if __name__ == '__main__':
    app.run(debug=True)
