# rcm_system

## Intro
This is just a repo for storing Recommender System engine codes and primary docs. This project main purpose is understanding different kinds of basic Recommender Systems, their basic algorithms and functions and their implementation and evaluation. in the other part implementing Neo4j database for User_Item dataset which as a graph database (maybe) gives us different benefits in next moves.
* This project is performed for a R&D part of a company, So as it has just research approach it doesn't designed for industrial implementation.
* for testing our engine we use (as usual!) Netflix rating dataset that was published for Netflix Prize Contest and you can download it via this link.

## Primary Designing
As mentioned we want to implement RCM engine. so each user with different datasets should be able to implement this engine on his/her target dataset and with giving this dataset as an input, evaluate different recommendation algorithms on his/her dataset.
So as an Input Model Class get two matrix in Pandas Dataframe format.(todo: link to pandas) 
