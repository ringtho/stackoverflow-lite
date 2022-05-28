# StackOverflow-lite 

[![CircleCI](https://circleci.com/gh/ringtho/stackoverflow-lite/tree/api.svg?style=shield)](https://circleci.com/gh/ringtho/stackoverflow-lite/?branch=api)  [![Maintainability](https://api.codeclimate.com/v1/badges/f8432418761ae69b0fe8/maintainability)](https://codeclimate.com/github/ringtho/stackoverflow-lite/maintainability)  [![Coverage Status](https://coveralls.io/repos/github/ringtho/stackoverflow-lite/badge.svg?branch=api)](https://coveralls.io/github/ringtho/stackoverflow-lite?branch=api) 


## Overview
StackOverflow-lite is a platform where people can ask questions and provide answers.

This StackOverflow-lite Api serves to create, edit, delete and retrieve questions and answers provided by other users.
The endpoints are deployed at [StackOverflow-lite Heroku](https://stackoverflow-lite-flask.herokuapp.com/apidocs)

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
The StackOverflow-lite API is implemented in flask, a python microframework. Version 1 of the API is hosted on Heroku and can be accessed at [StackOverflow-lite Heroku](https://stackoverflow-lite-flask.herokuapp.com/apidocs)
The corresponding endpoints and their functionalities are described below

|Endpoint                                       | Function                          
|-----------------------------------------------|----------------------------------------------
|POST /questions                                    | adds a question to the database(list)
|GET /questions                                     | retrieves all questions stored in the database
|GET /questions/<question_id>                       | retrives a particular question based on its id
|GET /questions/<username>                          | retrieves all questions of a particular author
|PUT /questions/<question_id>                       | edits a unique question based on it's id 
|DELETE /questions/<question_id>                    | deletes a question based on it's id
|POST /questions/<question_id>/answers              | adds a answer to a particular question
|PUT /questions/<question_id>/answers/<answer_id>   | marks an answer as preferred
|GET /questions/<question_id>/answers/<answer_id>   | retrieves a particular answer to a question
|DELETE /questions/<question_id>/answers/<answer_id> | deletes an answer based on it's id
|POST /questions/<question_id>/answers/<answer_id>/comments | adds a comment to an answer
|GET /questions/<question_id>/answers/<answer_id>/comments/<comment_id> | retrieves a particular comment
|PUT /questions/<question_id>/answers/<answer_id>/comments/<comment_id> | edits a comment based on it's id
|DELETE /questions/<question_id>/answers/<answer_id>/comments/<comment_id> | deletes a particular comment

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
* Use the link below to fork the app on postman.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/6160484-8d07d5c1-730d-4786-b12f-ace574dfea7d?action=collection%2Ffork&collection-url=entityId%3D6160484-8d07d5c1-730d-4786-b12f-ace574dfea7d%26entityType%3Dcollection%26workspaceId%3Db626a45c-b310-423e-9f53-cc578f23bb7d)

## Contributors
* Ringtho Smith - *sringtho@gmail.com*
