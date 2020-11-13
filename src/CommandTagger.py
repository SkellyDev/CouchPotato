
import nltk

TREE_LST = [(7, 13), (43, 17), (38, 11), (7, 50)]
HOUSE = [(30, 30), (40, 40)]
LAKE = [(10, 20), (15, 25)]


class CommandTagger:
    def __init__(self, RawCommand):
        self.RawCommand = RawCommand

    def get_full_tag_list(self, func: str):
        tags = nltk.pos_tag(nltk.word_tokenize(self.RawCommand))
        if func == 'find_closest_animal':
            for i in tags:
                nn = i[0].lower()
                if i[1] == 'NN' and nn in ['house', 'lake', 'tree', 'trees']:
                    if nn == 'house':
                        return HOUSE
                    elif nn == 'tree' or nn == 'trees':
                        return TREE_LST
                    else:
                        return LAKE
                else:
                    return "agent"

        elif func == 'get_direction_of_entity_relative_agent':
            for i in tags:
                nn = i[0].lower()
                if i[1] == 'NN' and nn in ['cow', 'sheep', 'pig']:
                    if nn == 'cow':
                        return 'Cow'
                    elif nn == 'sheep':
                        return 'Sheep'
                    else:
                        return 'Pig'
        elif func == 'get_direction_of_entity_relative_block':
            animal = ""
            block = ""
            for i in tags:
                nn = i[0].lower()
                if i[1] == 'NN' and nn in ['house', 'lake', 'tree', 'trees']:
                    if nn == 'house':
                        block = HOUSE
                    elif nn == 'tree' or nn == 'trees':
                        block = TREE_LST
                    else:
                        block = LAKE
                if i[1] == 'NN' and nn in ['cow', 'sheep', 'pig']:
                    if nn == 'cow':
                        animal = 'Cow'
                    elif nn == 'sheep':
                        animal = 'Sheep'
                    else:
                        animal = 'Pig'
            return animal, block
        else:
            pass
