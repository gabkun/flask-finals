from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.utils  # Correctly import the utils module
import json

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('data.csv')

@app.route('/')
def index():
    # Summary statistics
    survival_rate = df['Survived'].mean() * 100
    class_distribution = df['Pclass'].value_counts().to_dict()
    return render_template('index.html', 
                           survival_rate=round(survival_rate, 2), 
                           class_distribution=class_distribution)

@app.route('/charts')
def charts():
    # Create a survival bar chart
    survival_chart = px.bar(
        df['Survived'].value_counts(),
        labels={'index': 'Survived', 'value': 'Count'},
        title="Survival Distribution"
    )
    survival_chart_json = json.dumps(survival_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Create an age distribution histogram
    age_histogram = px.histogram(
        df, x='Age', nbins=20, title="Age Distribution",
        labels={'Age': 'Age', 'count': 'Count'}
    )
    age_histogram_json = json.dumps(age_histogram, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({
        'survival_chart': survival_chart_json,
        'age_histogram': age_histogram_json
    })

@app.route('/data')
def data():
    search = request.args.get('search', '')
    filtered_df = df[df['Name'].str.contains(search, case=False)] if search else df
    return filtered_df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
