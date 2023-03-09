import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from .models import MyUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from premium.models import Premium

from graphql_jwt.shortcuts import create_refresh_token, get_token
import graphql_jwt

class MyUserType(DjangoObjectType):
    class Meta:
        model = MyUser

class Query(ObjectType):
    pass


class MyUserInput(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String()
    password = graphene.String(required=True)


class CreateMyUser(graphene.Mutation):
    class Arguments:
        input = MyUserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(MyUserType)
    token = graphene.String()
    
    @staticmethod
    def mutate(root, info, input=None):  

        username=input.username  
        email=input.email  
        password=input.password 
        
        email_user = MyUser.objects.filter(email=email).values().first()        
        if email_user is None:
            username_user = MyUser.objects.filter(username=username).values().first()            
            if username_user is None:
                ok = True        
                user = MyUser.objects.create_user(email=email, password=password, username=username)
                token = get_token(user)
                user.save()
                return CreateMyUser(ok=ok, user = user, token = token)
            raise GraphQLError('El usuario ya existe') 
        raise GraphQLError('El email ya esta siendo usado')


class UpdateMyUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MyUserInput(required=True)
                
    ok = graphene.Boolean()
    user = graphene.Field(MyUserType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id, input=None):
        user_instance = MyUser.objects.get(pk = id)
                        
        if user_instance:
            ok = True
            user_instance.username = input.username
            user_instance.email = input.email
            user_instance.password = input.password
            user_instance.save()
            return UpdateMyUser(ok=ok, user = user_instance)
        raise GraphQLError('Usuario no encontrado')


class PremiumUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String(required=True)
        tarjeta = graphene.Int(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(MyUserType)
    tarjeta = graphene.Int()

    @staticmethod
    def mutate(root, info, email, password, tarjeta):
        user = MyUser.objects.get(email=email)
        
        if user:
            ok = True            
            content_type = ContentType.objects.get_for_model(Premium)
            permission = Permission.objects.get(
                codename='view_premium',
                content_type=content_type
            )                 
            user.user_permissions.add(permission)            
            user.save()
            return PremiumUser(ok=ok, user=user)
        raise GraphQLError('Usuario no encontrado')



class Mutation(graphene.ObjectType):
    create_my_user = CreateMyUser.Field()
    update_my_user = UpdateMyUser.Field()
    premiun_user = PremiumUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)