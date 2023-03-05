import graphene
from .models import Premium
from user.models import MyUser
from graphene_django.types import DjangoObjectType, ObjectType


class PremiumType(DjangoObjectType):
    class Meta:
        model = Premium

class Query(ObjectType):
    ingredient_premium = graphene.Field(PremiumType, email = graphene.String(required=True))
    all_ingredient_premium = graphene.List(PremiumType, email = graphene.String(required=True))
          
    def resolve_ingredient_premium(self, info, **kwargs):
        email = kwargs.get('email')
        user = MyUser.objects.get(email=email)
       
        if user.has_perm('premium.view_premium'):
            return Premium.objects.get(user_id=user.id)
        return None

    def resolve_all_ingredient_premium(self, info, **kwargs):
        email = kwargs.get('email')
        user = MyUser.objects.get(email=email)
       
        if user.has_perm('premium.view_premium'):
            return Premium.objects.all()
        return None
    
   

schema = graphene.Schema(query=Query)