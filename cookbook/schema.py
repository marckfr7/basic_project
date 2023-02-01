import graphene
from graphene_django import DjangoObjectType
from ingredients.models import Category, Ingredient
from ingredients import schema

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ['id', 'name', 'ingredients']

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'notes', 'category']

class Query(schema.Query, graphene.ObjectType):
   pass

class Mutation(schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)