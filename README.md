# Soft Desk API

This API was made to let a community of user create project, issues and comment.

See all end point here : [PostMan](https://go.postman.co/workspace/My-Workspace~292abc91-c319-4938-8789-b7099f5ce8d8/collection/18181285-49b39fbf-0f94-4906-8df5-36ef68fc7b59)

# Language used

This website was devellop with [Python](https://www.python.org/)(3.9.7)

# Virtual Environement

To install the virtual environement:

## With Linux/Mac
<hr/>
Install :

    python3 -m venv .venv

Activate :

    source .venv/bin/activate

## With Windows
<hr/>

Install : 

    py -3 -m venv .venv

Activate :

    .venv/scripts/activate

# Package et modules


Intsall all the dependncies with one step with [pip](https://fr.wikipedia.org/wiki/Pip_(gestionnaire_de_paquets)) :

    pip install -r requirements.txt

# Execute the server

This command should be execute in the SoftDesk folder in order to start the server in localhost

    python manage.py runserver
