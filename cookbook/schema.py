import graphene
from graphene_django import DjangoObjectType
from ingredients.models import Category, Ingredient
from ingredients import schema
from user import schemas


class Query(schema.Query, schemas.Query, graphene.ObjectType):
    pass

class Mutation(schema.Mutation, schemas.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)