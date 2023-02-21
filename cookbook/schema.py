import graphene
from graphene_django import DjangoObjectType
from ingredients.models import Category, Ingredient
from ingredients import schema

class Query(schema.Query, graphene.ObjectType):
   pass

class Mutation(schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)