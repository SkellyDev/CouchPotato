'''
This is a script for parsing command 
and pass it as input for action script
to call correct method
'''
import nltk
import json
import numpy
import tensorflow
import tflearn
from nltk.stem.lancaster import LancasterStemmer
nltk.download('punkt')
stemmer = LancasterStemmer()

with open("input.json") as file:
    DATA = json.load(file)


class CommandParse:
    def __init__(self, RawCommand):
        self.raw_command = RawCommand
        self.parse = ""

    def return_model(self):
        tag_lst = sorted([dicts["tag"] for dicts in DATA["commands"]])
        all_word_lst = []  # all word in one list
        tag_word_lst = []  # word list for each pattern
        tag_lst_y = []
        for dicts in DATA["commands"]:
            for pattern in dicts["patterns"]:
                tag_word_lst.append(nltk.word_tokenize(pattern))
                all_word_lst.extend(nltk.word_tokenize(pattern))
                tag_lst_y.append(pattern["tag"])

        all_word_lst = [stemmer.stem(word.lower())
                        for word in all_word_lst if word != "?"]
        all_word_lst = sorted(list(set(all_word_lst)))
    
        training = []  # for each tag, have a bag of word
        output = []
        out_empty = [0 for _ in range(len(tag_lst))]
        for index, tag_word in enumerate(tag_word_lst):
            bag = []
            twl = [stemmer.stem(word.lower()) for word in tag_word]
            for w in all_word_lst:
                if w in twl:
                    bag.append(1)
                else:
                    bag.append(0)
            training.append(bag)
            # find which label
            tag = tag_lst.index(tag_lst_y[index])
            output_row = out_empty[:]
            output_row[tag] = 1
        training = numpy.array(training)
        output = numpy.array(output)

        # ----- nn --------
        tensorflow.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 4)
        net = tflearn.fully_connected(net, 4)
        net = tflearn.fully_connected(
            net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        model.fit(training, output, n_epoch=1000,
                  batch_size=4, show_metric=True)
        model.save("model.tflearn")
        return model, all_word_lst, tag_lst

        def parse_command(self, user_command):
            model = self.return_model()[0]
            all_word_lst = self.return_model()[1]
            bag = [0 for _ in range(len(all_word_lst))]

            user_word = nltk.word_tokenize(user_command)
            user_word = [stemmer.stem(w.lower()) for w in user_word]
            for w in user_word:
                for index, word in enumerate(all_word_lst):
                    if w==word:
                        bag[i] = 1
            return numpy.array(bag)

