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
<p><img src="assets/ct.png" width="650" alt/><em>Figure 1: Sample Constituency Tree </em></p>
The linearized version of the above parse tree looks as '(SBARQ (WHNP (WP what)) (S (VP (VBZ is) (NP (NP (DT the) (JJS closest) (NN animal)) (PP (IN near) (NP (DT the) (NN house)))))))'


### Environmental Describing Function

## Evaluation

## References
