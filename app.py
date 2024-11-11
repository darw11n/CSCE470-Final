from flask import Flask, render_template, request, jsonify
from NaiveBayes import NaiveBayes
from coreAlgo import load_data, get_labels
import json
import os
from collections import defaultdict
import datetime


app = Flask(__name__)

# Load publication dates grouped by tag
def load_publication_dates_by_tag(folder_path):
    articles_by_tag = defaultdict(list)
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                articles = json.load(file)
                for article in articles:
                    tag = filename.replace('.json', '')  # Assuming filename is tag name
                    pub_date = article.get("publication_date")
                    if pub_date:
                        # Parse date
                        date_obj = datetime.datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ")
                        articles_by_tag[tag].append(date_obj.isoformat())
    return articles_by_tag

# Load your dataset, train the model
# Assuming you have a training function here
def load_and_train():
    # Your loading and training code here
    # For example:
    dataset = load_data("articles_json/")
    labels = get_labels("articles_json/")
    classifier = NaiveBayes(labels)
    classifier.train(dataset)
    return classifier

classifier = load_and_train()

@app.route('/')
def home():
    return render_template('index.html')

# Route for prediction page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        text = request.form['text']
        prediction = classifier.predict(text)
        return render_template('predict.html', prediction=prediction, text=text)
    return render_template('predict.html')

# Route for visualization page
@app.route('/visualize')
def visualize():
    # Get tag distribution and average document length per tag
    articles_per_tag = classifier.n_doc
    avg_length_per_tag = {
        label: classifier.total_words_in_class[label] / max(1, articles_per_tag[label])
        for label in classifier.Labels
    }
    publication_dates_by_tag = load_publication_dates_by_tag("articles_json/")
    # Package data to be JSON-serializable
    data = {
        "articles_per_tag": articles_per_tag,
        "avg_length_per_tag": avg_length_per_tag,
        "publication_dates": publication_dates_by_tag
    }
    return render_template('visualize.html', data = json.dumps(data))

if __name__ == '__main__':
    app.run(debug=True)