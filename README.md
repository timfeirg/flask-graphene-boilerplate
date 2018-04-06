As a child, I always dreamed of writing solely CRUD operations and HTTP APIs will just be magically available, now I can finally achieve this with graphql.

This project demonstrates how to use Flask + [Flask-GraphQL](http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/#creating-graphql-and-graphiql-views-in-flask) to make a simple web app with simple CRUD operations, also includes some of the most basic tests.

## Setup everything and run the flask app

On a Mac of course.

```shell
brew install python3
pip install -U virtualenv virtualenvwrapper
mkvirtualenv graphene --python=python3

pip install -U -r requirements-dev.txt
mysql -uroot -e 'create database graphene_boilerplate'
py.test -s

./shell
> db.create_all()
> exit

export FLASK_APP=graphene_boilerplate/app.py
flask run --reload --port 5000
```

Now open up http://localhost:5000/graphql to play with GraphQL, see below for some example queries:

To create a `Item`:

```graphql
mutation see_if_create_works {
  createItem(key: "whatever", value: "{\"foo\": \"bar\"}") {
    ok
    item {
      id_
      key
      value
    }
  }
}
```

To list all `Item`:

```graphql
query {
  allItems {
    edges {
      node {
        id_
        key
        value
      }
    }
  }
}
```
