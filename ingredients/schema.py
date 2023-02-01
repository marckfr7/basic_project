import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Category, Ingredient
from graphql_relay import from_global_id

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )

class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
            "name": ['exact', 'icontains', 'istartswith'],
            "notes": ['exact', 'icontains'],
            "category": ['exact'],
            "category__name": ['exact'],
        }
        interfaces = (relay.Node, )

class Query(ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_category = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredient = DjangoFilterConnectionField(IngredientNode)


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    

class IngredientInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    notes = graphene.String()
    category = graphene.List(CategoryInput)

class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required = True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_instance = Category(name=input.name)
        category_instance.save()
        return CreateCategory(ok=ok, category=category_instance)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CategoryInput(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryNode)

    @staticmethod
    def mutate(root, info, id, input=None,):
        category_instance = Category.objects.get(pk=id)

        if category_instance:
            ok = True
            category_instance.name = input.name
            category_instance.save()
            return UpdateCategory(ok=ok, category=category_instance)
        return UpdateCategory(ok=ok, category=None)

class CreateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientInput (required=True)

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_array = []
        for item_categorys in input.category:
            categorys = Category.objects.get(pk=item_categorys.id)
            if categorys is None:
                return CreateIngredient(ok=False, ingredient=None)
            category_array.append(categorys) 
            ingredient_instance = Ingredient(name=input.name)     
            ingredient_instance.notes = notes=input.notes   
            print(ingredient_instance)
            ingredient_instance.save()
            print("hola")
            ingredient_instance.category.set(category_array)
            return CreateIngredient(ok=ok, ingredient=ingredient_instance)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_ingredien = CreateIngredient.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)