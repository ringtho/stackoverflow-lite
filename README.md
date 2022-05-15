# StackOverflow-lite 

[![CircleCI](https://circleci.com/gh/ringtho/stackoverflow-lite.svg?style=svg)](https://circleci.com/gh/ringtho/stackoverflow-lite)


## Overview
StackOverflow-lite is a platform where people can ask questions and provide answers.

This StackOverflow-lite Api serves to create, edit, delete and retrieve questions and answers provided by other users.
The endpoints are deployed at [iReporter Heroku](https://sringtho.herokuapp.com)

# Features

A user can:

- create an account and login.
- can post questions
- can delete the questions they post
- can post answers
- can view the answers to questions
- can accept an answer out of all the answers to his/her questions as the preferred answer
- can upvote or downvote an answer
- can comment on an answer
- can fetch all questions he/she has ever asked on the platform
- can search for questions on the platform
- can view questions with the most answers

## API Description ##
The StackOverflow-lite API is implemented in flask, a python microframework. Version 1 of the API is hosted on Heroku and can be accessed at https://sringtho.herokuapp.com.
The corresponding endpoints and their functionalities are described below

|Endpoint                                       | Function                          
|-----------------------------------------------|----------------------------------------------
|POST /questions                                    | adds a question to the database(list)
|GET /questions                                     | retrieves all questions stored in the database
|GET /questions/<question_id>                       | retrives a particular question based on its id
|PUT /questions/<question_id>                       | edits a unique question based on it's id 
|DELETE /questions/<question_id>                    | deletes a question based on it's id
|POST /questions/<question_id>/answers              | adds a answer to a particular question
|PUT /questions/<question_id>/answers/<answer_id>   | marks an answer as preferred

When using the API and example of the input data for creating a question is shown below:
```javascript
{
    "id": 2,
    "question": "Django Rest Framework",
    "description": "Whenever I am logging in I get an error that affects my applicati",
    "stack": "Django, Python"
}
```

## Installation Instructions
To run the API, follow these steps:
* Clone this repository onto your computer
* Install python3 and postman
* Navigate to the repository root (stackoverflow-lite) and create a virtual environment
```
$ cd stackoverflow-lite
$ python3 -m venv venv
```
* Activate the virtual environment and install dependencies in requirements.txt
```
$ source venv/bin/activate
$ pip install -r requirements.txt
```
* Run the app.py script
```
$ python app.py
```
* Test the API endpoints using Postman

## Contributors
* Ringtho Smith - *sringtho@gmail.com*
