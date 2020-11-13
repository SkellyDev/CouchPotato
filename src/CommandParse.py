'''
This is a script for parsing command 
and pass it as input for action script
to call correct method
'''
import json
import nltk
import numpy
import random
from tensorflow.python.framework import ops
import tflearn
import pickle

from nltk.stem.lancaster import LancasterStemmer

nltk.download('punkt')
stemmer = LancasterStemmer()


class CommandParse:
    def __init__(self, RawCommand):
        self.raw_command = RawCommand
        self.words = []
        self.labels = []

    def bag_of_words(self, s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)

    def get_words(self):
        return self.words

    def get_labels(self):
        return self.labels

    def save_model(self):
        nltk.download('punkt')
        stemmer = LancasterStemmer()

        with open('input.json') as file:
            data = json.load(file)

        try:
            with open("data.pickle", "rb") as f:
                self.words, self.labels, training, output = pickle.load(f)
        except:

            docs_x = []
            docs_y = []

            for intent in data["commands"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    self.words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent["tag"])

                if intent["tag"] not in self.labels:
                    self.labels.append(intent["tag"])

            self.words = [stemmer.stem(w.lower())
                          for w in self.words if w != "?"]
            self.words = sorted(list(set(self.words)))

            self.labels = sorted(self.labels)

            training = []
            output = []

            out_empty = [0 for _ in range(len(self.labels))]

            for x, doc in enumerate(docs_x):
                bag = []

                wrds = [stemmer.stem(w.lower()) for w in doc]

                for w in self.words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)

                output_row = out_empty[:]
                output_row[self.labels.index(docs_y[x])] = 1

                training.append(bag)
                output.append(output_row)

            training = numpy.array(training)
            output = numpy.array(output)

            with open("data.pickle", "wb") as f:
                pickle.dump((self.words, self.labels, training, output), f)

        ops.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 6)
        net = tflearn.fully_connected(net, 6)
        net = tflearn.fully_connected(
            net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        model.fit(training, output, n_epoch=1000,
                  batch_size=6, show_metric=True)
        model.save("model.tflearn")
        return model

    def return_tag(self, model, words, labels):
        inp = self.raw_command

        model.load("model.tflearn")
        results = model.predict([self.bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        return tag
