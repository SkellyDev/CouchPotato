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
        self.treenode = TreeNode
        self.nodeStack = []
        self.nn = []
        self.visit(TreeNode)
        self.call_function()

    def visit(self, node):
        for n in node.children:
            if n not in self.nodeStack:
                # print(n.label)
                self.nodeStack.append(n)  # w p np

        if node.label == "SBARQ" or node.label == "SBAR":
            return self.visit_sbarq(node)
        elif node.label == "NN" or node.label == 'NNS':
            return self.visit_nn(node)
        elif node.label == "S":
            return self.visit_s(node)
        elif node.label == "VB":
            return self.visit_vb(node)
        elif node.label == "IN" and "how many" not in self.treenode.children[0].text.lower() and node.text.lower() not in ["near", "to", "of"]:
            return self.visit_in(node)
        else:
            #print("node label", node.label)
            if node in self.nodeStack:
                i = self.nodeStack.index(node)
                self.nodeStack.pop(i)
            if len(self.nodeStack) > 0:
                new = self.nodeStack.pop(0)
                self.visit(new)

    def visit_sbarq(self, n):
        if n.children[0].text.lower() == "where":
            self.tag = "direction"
        elif n.children[0].text.lower() == "what":
            self.tag = "nearest"
        elif re.findall('\w+\s{1}\w+', n.text.lower())[0] == "how many":
            self.tag = "count"
        return self.visit(n.children[1])

    def visit_nn(self, n):
        a = n.text
        self.nn.append(a)
        if len(self.nodeStack) > 0:
            ne = self.nodeStack.pop(0)
            return self.visit(ne)

    def visit_in(self, n):
        self.tag = "inside"
        if len(self.nodeStack) > 0:
            ne = self.nodeStack.pop(0)
            return self.visit(ne)

    def visit_s(self, n):
        '''陈述句'''
        return self.visit(n.children[0])

    def visit_vb(self, n):
        self.tag = "describe"

    def call_function(self):
        if self.tag == "describe":
            return self.CA.describe_agent_location()

        if self.nn[0].lower() == "direction":
            self.tag = "direction"
            self.nn.pop(0)

        if self.tag == "direction":
            if len(self.nn) == 1:
                print(self.CA.getDirection(self.nn[0]))
            else:
                print(self.CA.getDirection(self.nn[0], self.nn[1]))

        elif self.tag == "nearest":
            if len(self.nn) == 1:
                print(self.CA.closest())
            else:
                if self.nn.count("animal") > 1:
                    num = self.nn.count("animal")
                    #print('self.nn.count("animal")', num)
                    param = self.nn[-1] if self.nn[-1] != "animal" else "agent"
                    while num > 0:
                        param = self.CA.closest(param)
                        #print('return result param', param)
                        num -= 1
                    print("The closest animal is", param)
                else:
                    print("The closest animal is", self.CA.closest(self.nn[1]))

        elif self.tag == "count":
            return self.CA.count(self.nn[0], self.nn[1])

        elif self.tag == "inside":
            inside = self.CA.inside(self.nn[1])[1]
            print(inside)
