import math

class NaiveBayes:
    def __init__(self, Labels):
    
        self.Labels = Labels
        self.n_doc_total = 0
        self.n_doc = {l: 0 for l in Labels}
        self.vocab = {l: {} for l in Labels}
        
        #Added addt'l class attributes to speed up prediction speed
        self.total_words_in_class = {l: 0 for l in Labels}
        self.vocab_set = set()

    def train(self, ds):
        terms_set = set()
        for document in ds:
            word_list = [word.lower() for word in document[1].split(" ")]
            terms_set.update(word_list)
        
        terms_set = sorted(terms_set)
        self.vocab_set = terms_set

        for label in self.Labels:
            for word in terms_set:
                self.vocab[label][word] = 0

        for document in ds:
            for word in document[1].split(" "):
                self.vocab[document[2]][word.lower()] += 1
            self.n_doc_total += 1
            self.n_doc[document[2]] += 1
        
        # Precompute total words per class in train so you don't have to do it again every time for prediction
        for label in self.Labels:
            self.total_words_in_class[label] = sum(self.vocab[label].values())

    def predict(self, x):
        label_scores = {label: 0 for label in self.Labels}
        
        for label in self.Labels:
            prob_of_class = self.n_doc[label] / self.n_doc_total
            prob_of_word_sum = 0
            
            # Split and preprocess once for each document
            words = [word.lower() for word in x.split(" ")]

            for word in words:
                numerator = self.vocab[label].get(word, 0) + 1
                denominator = self.total_words_in_class[label] + len(self.vocab_set)
                prob_of_word_sum += math.log(numerator / denominator)

            label_scores[label] = math.log(prob_of_class) + prob_of_word_sum
        
        return max(label_scores, key=label_scores.get)


