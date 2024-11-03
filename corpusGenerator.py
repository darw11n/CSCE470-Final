import requests
import matplotlib.pyplot as plt
from collections import defaultdict
import datetime
import numpy as np
import random
import json
import csv
import os

API_KEY = '#' #Replace with your own API key to use

BASE_URL = 'https://content.guardianapis.com/'


def get_articles_by_tag(api_key, tag_id, target_articles, page_size=200):
    url = f"{BASE_URL}search"
    article_bodies = []
    total_fetched = 0  
    page = 1
    
    while total_fetched < target_articles:
        params = {
            'api-key': api_key,
            'tag': tag_id,    
            'show-fields': 'body',  
            'page-size': min(page_size, target_articles - total_fetched), 
            'page': page  
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            articles = response.json().get('response', {}).get('results', [])
            for article in articles:
                body_text = article['fields'].get('body', 'No text available')
                article_bodies.append({
                    'title': article['webTitle'],
                    'section': article['sectionName'],
                    'publication_date': article['webPublicationDate'],
                    'url': article['webUrl'],
                    'body': body_text
                })
            total_fetched += len(articles)
            print(f"Fetched page {page} for tag {tag_id} with {len(articles)} articles.")
        else:
            print(f"Error: {response.status_code} on page {page} for tag {tag_id}")
            break
        
        if len(articles) == 0:  
            break
        
        page += 1
    
    # If we fetch more articles than needed (e.g., on the last page), trim the excess
    return article_bodies[:target_articles]


def get_articles_from_multiple_tags(api_key, tags):
    all_articles = {}
    for tag in tags:
        random_article_count = random.randint(900, 1000)  # Random number of articles, no real reason 
        print(f"Fetching {random_article_count} articles for tag: {tag}")
        articles = get_articles_by_tag(api_key, tag, target_articles=random_article_count)
        all_articles[tag] = articles
    return all_articles

#Distribution of tags (Number of articles per tag)
def visualize_tag_distribution(articles_by_tag):
    tag_names = list(articles_by_tag.keys())
    article_counts = [len(articles) for articles in articles_by_tag.values()]

    plt.figure(figsize=(10, 6))
    plt.barh(tag_names, article_counts, color='skyblue')
    plt.xlabel('Number of Articles')
    plt.ylabel('Tags')
    plt.title('Distribution of Articles by Tag')
    plt.show()

# Average document length per tag
def visualize_avg_length_per_tag(articles_by_tag):
    tag_names = []
    avg_lengths = []
    
    for tag, articles in articles_by_tag.items():
        lengths = [len(article['body'].split()) for article in articles if article['body']]
        avg_length = np.mean(lengths)
        tag_names.append(tag)
        avg_lengths.append(avg_length)

    plt.figure(figsize=(10, 6))
    plt.barh(tag_names, avg_lengths, color='lightgreen')
    plt.xlabel('Average Length (Words)')
    plt.ylabel('Tags')
    plt.title('Average Document Length by Tag')
    plt.show()

# Publication date distribution
def visualize_publication_date_distribution(articles_by_tag):
    tag_dates = defaultdict(list)
    
    for tag, articles in articles_by_tag.items():
        for article in articles:
            pub_date = article['publication_date']
            if pub_date:
                date_obj = datetime.datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%SZ')
                tag_dates[tag].append(date_obj)

    plt.figure(figsize=(12, 8))
    for tag, dates in tag_dates.items():
        dates = sorted(dates)
        plt.hist(dates, bins=20, label=tag, alpha=0.6)

    plt.xlabel('Publication Date')
    plt.ylabel('Number of Articles')
    plt.title('Publication Date Distribution by Tag')
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.show()

# Function to save articles by tag to JSON
def save_articles_to_json(articles_by_tag, output_dir='articles_json'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for tag, articles in articles_by_tag.items():
        filename = os.path.join(output_dir, f"{tag.replace('/', '_')}_articles.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(articles)} articles for tag {tag} to {filename}")

# Function to save articles by tag to CSV
def save_articles_to_csv(articles_by_tag, output_dir='articles_csv'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for tag, articles in articles_by_tag.items():
        filename = os.path.join(output_dir, f"{tag.replace('/', '_')}_articles.csv")
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'section', 'publication_date', 'url', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for article in articles:
                writer.writerow({
                    'title': article['title'],
                    'section': article['section'],
                    'publication_date': article['publication_date'],
                    'url': article['url'],
                    'body': article['body']
                })
        print(f"Saved {len(articles)} articles for tag {tag} to {filename}")

tags = [
    "football/football", "politics/politics", "science/science", "environment/environment", 
    "technology/technology", "world/world", "sport/sport", "business/business", "culture/culture"
]

articles_by_tag = get_articles_from_multiple_tags(API_KEY, tags)

visualize_tag_distribution(articles_by_tag)

visualize_avg_length_per_tag(articles_by_tag)

visualize_publication_date_distribution(articles_by_tag)

save_articles_to_json(articles_by_tag)
save_articles_to_csv(articles_by_tag)