'''
This is a script for parsing command 
and pass it as input for action script
to call correct method
'''
import nltk


class CommandParse:
    def __init__(self, RawCommand):
        self.raw_command = RawCommand
        self.parse = ""

    def parse_command(self):
        # Attenion!!!
        # return row command first before we finishing command parsing part
        tagged = nltk.pos_tag(nltk.word_tokenize(self.raw_command))
        return tagged
