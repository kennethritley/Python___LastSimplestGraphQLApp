'''
The next simplest possible Python script that shows GraphQL in action.
This one shows what GraphQL was invented for, namely, you can ask
for specific data and GraphQL will send back specifically what you ask for.

Author: KEN
Date:   2023.04.26
'''

import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from flask_graphql import GraphQLView
import graphene

class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    age = graphene.Int()
    email = graphene.String()

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())

    def resolve_user(self, info, id):
        # Simulate fetching user data by ID
        users = {
            1: User(id=1, name="Roger", age=37, email="roger@example.com"),
            2: User(id=2, name="Tina", age=57, email="tina@example.com"),
        }
        return users.get(id)

schema = graphene.Schema(query=Query)

# app = Flask(__name__)
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=False))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    user_id = request.form['user_id']
    query = f"""
    {{
        user(id: {user_id}) {{
            id
            name
            age
            email
        }}
    }}
    """

    # Use the following line instead of the requests.post call
    response_data = schema.execute(query).to_dict()

    if 'errors' in response_data:
        return "Error: User not found.", 404

    user_data = response_data['data']['user']
    return jsonify(user_data)

if __name__ == '__main__':
    app.run()
