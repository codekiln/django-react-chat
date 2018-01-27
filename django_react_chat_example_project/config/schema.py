import graphene

from django_react_chat_example_project.chat.schema import Query as ChatQuery


class Query(ChatQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
