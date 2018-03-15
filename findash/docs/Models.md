# Models

A model is a single, definite source of truth about your data. It contains the essential fields and behaviours of the data stored. The goal is to define the data model in one place and automatically derive things from it.

## Polls
In the polls app, we have created two models: ```Question``` and ```Choice```. A question has a question and a publication date. A Choice has two fields: the text of the choice and a vote tally. Each Choice is associated with a Question.

With that models.py, Django is able to create a database schema for this app, and create an API for accessing Question and Choice objects.
