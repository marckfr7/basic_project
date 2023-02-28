import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(ObjectType):
    category = graphene.Field(CategoryType, id = graphene.Int())
    ingredient = graphene.Field(IngredientType, id = graphene.Int())

    all_category = graphene.List(CategoryType)
    all_ingredient = graphene.List(IngredientType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')

        if id is None:
            return None
        return Category.objects.get(pk=id)

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')

        if id is None:
            return None
        return Ingredient.objects.get(pk=id)

    def resolve_all_category(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredient(self, info, **kwargs):
        return Ingredient.objects.all()

class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()

class IngredientInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    notes = graphene.String()
    category = graphene.Int()

class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

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
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = True
        category_instance = Category.objects.get(pk=id)

        if category_instance:
            category_instance.name = input.name
            category_instance.save()
            return UpdateCategory(ok=ok, category=category_instance)
        return UpdateCategory(ok=None, category=None)

class CreateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientInput(required=True)

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category = Category.objects.get(pk = input.category)
        
        if category is None:
            return CreateIngredient(ok = False, ingredient = None)
        ingredient_instance = Ingredient.objects.create(
            name= input.name, 
            notes= input.notes, 
            category_id= input.category
            )
        return CreateIngredient(ok = ok, ingredient = ingredient_instance)

class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        input = IngredientInput(required = True)

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, id, input = None):
        ok = False
        category = Category.objects.get(pk = input.category)
        if category is None:
            return UpdateIngredient(ok = ok, ingredient = None)

        ingredient_instance = Ingredient.objects.get(pk=id)        
        if ingredient_instance:            
            ok = True                       
            ingredient_instance.name = input.name            
            ingredient_instance.notes = input.notes            
            ingredient_instance.category_id = input.category            
            ingredient_instance.save()
            return UpdateIngredient(ok = ok, ingredient = ingredient_instance)
        return UpdateIngredient(ok = ok, ingredient = None)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)