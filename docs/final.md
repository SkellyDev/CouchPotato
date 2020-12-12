---
layout: default
title: Final Report
---

## Video

## Project Summary
The main goal of this project is to build an "environment-describing chatbot" which can understand users' questions about surrounding environment and answer expected information retrieved through Malmo API. To achieve this goal, we focused on two parts: the first part is natural language processing (NLP), and the second part is implement environment decribing functions to retrieve related information. 

The main challenge is that, instead of match our functions with specific language description/user questions, we want our NLP processing and functions can deal with language with greater scope and more flexible with asking questions. In other words, our chatbot needs to have a clear understanding on the individual parts of the speech and the dependencies in between, in order to connect user questions with correct environmental describing function and pass corresponding arguments. For instance, consider two questions: 

- "How many sheep are inside the house" 
- "What animals are inside the house" 

The meanings of these sentences are quite different, and our chatbot need to understand the first question is asking about "count(cows, inside(house))", and the second question is asking about "find(animals, inside(house))". In order to achieve this, using a deep learning model for NLP is necessary to help us to process the syntatic structure of user's question. We utilized AllenNLP constituency parsing tools into our project in order to get a syntatic tree model. 

Besides understanding users' question, we also need environment describing functions to ensure we return accurate information to our users. In this part, we deployed Malmo API to get basic environment information in the enviornment we build in Minecraft, and create purpose functions by using these information. Our projects can handle questions like, 

1. Find closest entity relative to agent architecture or other landscapes
2. Identify entity location relative to agent architecture or other landscapes
3. Count entities based on position
4. Describe current environment (such as find animals around the tree, and tell the location of the agent)

The challenge behind this part is that we need to be familiar and knowledgable enough to Malmo and efficiently convert the provided information to our environment describing function. 

## Approaches

### Natural Language Processing through Constituency Parsing
In this project, we utilize the AllenNLP constituency parsing to to understand the syntatic structure of user's question, and build a new tree to store the constituency tree based on our needs and visit the new tree matching it with our function. Below is the picture showing the constituency tree AllenNLP generated for us: <p><img src="assets/ct.png" width="650" alt/><em>Figure 1: Sample Constituency Tree </em></p>

The sample question of the above tree is "Where is the tree near the house", and the linearized version of the above contituency tree looks like '(SBARQ (WHADVP (WRB Where)) (SQ (VBZ is) (NP (NP (DT the) (NN tree)) (PP (IN near) (NP (DT the) (NN house))))))'. The basic idea is that we firstly build a new tree to store the contituency tree by pairing its label and covering texts. Then, we implement a tree vistor in order to go over all the tree and get part of the information we need to match with our functions and pass correct arguments. To accomplish that, we firstly pass the tree root to the visitor and use a stack structure to store the node's children. By recursively call visit on the children, we will go over all the node types, which we will ignore some useless labels/texts, and only extract information from valuable node. For instance, suppose we have a question like "Where is the cow near the house". We will firstly pass the tree node to our visitor, which is a node with label (SBARQ) and text "Where is the tree near the house". Then, by visiting its children node text, we will know it is a where question, so we match the question with our "getDirection(entity, target)" question. Then, we will recursively visit the node's children by pop(0) from our node stack structure and find "NN" label(noun) and pass it to our function. 

Here are some pseudocode for our TreeNode and TreeVisitor: 
```python
# store the constituency tree 
class TreeNode: 
    self.children = [] # to store all the Node
    self.label = "" # Node Label, e.g NN(Noun), NP(Noun Phrase) ... 
    self.text = "" # Node Text: text that certain label covering  e.g. IN - near, NN - house
    
    def find_label:
        #all label are capital letter begin after "(" and stop at blank space
    
    def find_node:
        #find node label by matching "(" with ")" and construct new node and add it into self.children
        
    def find_text:
        #use regex to find text begin with white space and end before ")" 
        
class TreeVisitor:
    self.nodeStack = [] #to store node children 
    
    def visit(n):
      for n in n.children:
        self.nodeStack.append(n) #if children not in nodeStack
      
      if node.label == "SBARQ":
          return self.visit_sbarq(n)
      elif node.label == "NN":
          return self.visit_nn(n)
      elif ....: 
      
      else:
          self.nodeStack.pop # to ignore useless node such as ("is", "the")
      ...
      
   def visit_sbarq(n):
      if n.children[0].text.lower() == "where":
            self.tag = "direction"
      return self.visit(n.children[1])
    
  def visit_nn(n):
      if self.tag == "direction":
            getDirection()
      elif ... 
```

### Environmental Describing Function

## Evaluation

## References
