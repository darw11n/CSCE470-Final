
import os
import json
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from NaiveBayes import NaiveBayes

Labels = []

# Preprocessing function
def preprocess(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabet characters
    text = text.lower()  # Convert to lowercase
    return text

# Load data and preprocess
def load_data(folder_path):
    dataset = []
    for file_name in os.listdir(folder_path):
        label = file_name.split("_")[0]
        Labels.append(label)
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r') as file:
            articles = json.load(file)
            for i, article in enumerate(articles):
                doc_id = f"{label}_{i}"
                body_text = preprocess(article['body'])
                dataset.append((doc_id, body_text, label))
                
    return dataset

# Load and prepare the dataset
dataset = load_data("articles_json/")

# Split dataset into training and testing sets (70/30)
train_data, test_data = train_test_split(dataset, test_size=0.3, random_state=17)

# Initialize and train the classifier
classifier = NaiveBayes(Labels)
classifier.train(dataset)

# Make predictions on test set
true_labels = []
predicted_labels = []
i = 0

for doc_id, body, label in test_data:
    true_labels.append(label)
    predicted_labels.append(classifier.predict(body))
    i += 1
    print( (i / len(test_data) ) * 100)

# Evaluate the classifier
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, average='weighted')
recall = recall_score(true_labels, predicted_labels, average='weighted')
f1 = f1_score(true_labels, predicted_labels, average='weighted')

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")