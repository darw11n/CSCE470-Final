from flask import Flask, render_template, request, jsonify
import json
import os
import re
import math
from NaiveBayes import NaiveBayes
from coreAlgo import load_data, get_labels

app = Flask(__name__)


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
    # Dummy data for visualization example
    visualization_data = {
        "label1": 100,
        "label2": 75,
        "label3": 125,
    }
    return render_template('visualize.html', data=visualization_data)

if __name__ == '__main__':
    app.run(debug=True)