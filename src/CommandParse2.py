import re
from CommandAction import CommandAction


class TreeNode:
    def __init__(self, string):
        self.string = string
        #print("string: ", self.string)
        self.children = []
        self.label = ""
        self.text = ""
        self.rest_string = ""
        if self.string[0] == "(":  # except leaf situation
            self.find_label()
        self.find_text()
        #print("label: ", self.label)
        #print("text: ", self.text)
        for sub_node in self.find_node():
            if sub_node[0].isalpha() == False:  # except leaf situation
                self.children.append(TreeNode(sub_node))

    def find_label(self):
        stop = self.string.index(" ")
        self.label = self.string[1:stop]
        self.rest_string = self.string[stop+1:]

    def find_node(self):
        counter = 0
        node_lst = []
        start = 0
        if self.rest_string != "" and self.rest_string[0].isalpha():  # leaf
            node_lst.append(self.rest_string.rstrip(")"))

        for i in range(len(self.rest_string)):
            if self.rest_string[i] == "(":
                counter += 1
            elif self.rest_string[i] == ")":
                counter -= 1
                if counter == 0:  # node complete
                    next_node = self.rest_string[start:i+1]
                    start = i+1
                    node_lst.append(next_node.lstrip(" "))
        #print("children: ", node_lst)
        return node_lst

    def find_text(self):
        node_lst = self.find_node()
        result = []
        for node in node_lst:
            result.extend(re.findall('\w+\)', node))
        self.text = node_lst[0] if result == [] else " ".join(
            [s.rstrip(')') for s in result])


class TreeVisitor:

    def __init__(self, TreeNode, agent):
        self.CA = CommandAction(agent)
        self.nodeStack = []
        self.visit(TreeNode)

    def visit(self, node):
        for n in node.children:
            if n not in self.nodeStack:
                # print(n.label)
                self.nodeStack.append(n)  # w p np

        if node.label == "SBARQ":
            return self.visit_sbarq(node)
        elif node.label == "NN":
            return self.visit_nn(node)
        else:
            #print("node label", node.label)
            if node in self.nodeStack:
                i = self.nodeStack.index(node)
                self.nodeStack.pop(i)
            new = self.nodeStack.pop()
            self.visit(new)

    def visit_sbarq(self, n):
        if n.children[0].text.lower() == "where":
            nn = self.visit(n.children[1])
            print(nn)
            result = self.CA.getDirection('cow')
            print(result)

    def visit_nn(self, n):
        return n.text
