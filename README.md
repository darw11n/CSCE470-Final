# CSCE470-Final
This gihub contains the code for my final project for CSCE 470: Information Retrieval. The purpose of this project is to develop a text classifier that will automatically label new articles into one of several predetermined labels. The text classifier employed for this project is the Naive Bayes classifier. 

## Requirements

```bash
$ pip install matplotlib
```

For data visualizations

```bash
$ pip install requests
```

For REST API fetch requests used to generate the corpus of documents

```bash
$ pip install scikit-learn
```

For train_test_split and evaluating the Naive Bayes algorithim.

```bash
$ pip install Flask==1.1.4
```

For running the server and hosting the website.

```bash
$ pip install markupsafe==2.0.1
```

Resolving a potential issue with Flask.


To easily install all requirements, a requirements text file has been added to the repo. You can install all requirements at once using pip install -r requirements.txt

## How to run

The first step in running the code is generating the corpus of documents. The file [corpusGenerator.py](corpusGenerator.py) runs the code to generate the corpus of documents. It retrives a mix of somewhere between 900-1000 articles from the Guardian website in 9 different labels, and deposits them in new folders articles_json/ and articles_csv/. To run this file, you will need to replace the API key in line 11 with your own API key from the Guardian website. You can generate your own API key at the [Guardian OpenPlatform](https://open-platform.theguardian.com/access/) development console.

To generate the corpus, run:

```bash
$ python3 corpusGenerator.py
```

After the corpus is generated, the core algorithim is implemented in the files [coreAlgo.py](coreAlgo.py) and [NaiveBayes.py](NaiveBayes.py). The code will train on a randomly selected 70% of the corpus and predict on the remaining 30%.
```bash
$ python3 coreAlgo.py
```

Now, to demonstrate the hosted deployement of the server, run:


```bash
$ python3 -m flask run
```

This will launch the flask app from app.py, allowing you interact with the algorithim and visualize the data.

