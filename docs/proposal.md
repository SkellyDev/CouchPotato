# Proposal 

## Summary of the Project 
Our project will include two main parts: language navigation and environment description. Both these parts are related with Natural Language Processing (NLP) area. For the language navigation part, we will use terminal to give commands, telling the agent what following action are expected from him to do. These actions will include but not limit to: move to the furthest object in your view, move towards the river, move back of the house. In this project, we also expect the agent to describe his following environemnt by answering our questions typed in terminal. These questions will include: "how many pigs can you see in your view", "what is the direction of the river". We will work with the Malmo platform as well in order to let our agent make corresponding actions. 

## AI/ML Algorithms
NLTK: tokenization and wordnet 

## Evaluation Plan 
### Quantitative 
Since our agent is asked to follow the user input commands, we will evaluate our success rate based on how accurate our agent understands the content of the command, as well as the corresponding time. In most cases, one action or a series of actions could be described in many different ways in synonyms words. To make our results more accurate, we will need to match different expressions to the same object or verbs to the actual action function which our agent could perform. If any action does not follow the correct comprehension of our command, we will modify the word similarity algorithm and add that word into the previous module. For describing the world based on the question user asked, we will evaluate the success rate based on both how our agent understands the question and check whether the answer is correct based on the current given range of the scenery.

### Qualitative 
We will expect the agent to make right action and describe environment with correct information. 

## Appointment
2pm, Wednesday, Oct 28th, 2020


