import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from .models import MyUser
from .utils import create_acces_token, create_refresh_token
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from premium.models import Premium

class MyUserType(DjangoObjectType):
    class Meta:
        model = MyUser


class Query(ObjectType):
    user = graphene.Field(MyUserType, email = graphene.String(), password=graphene.String())    
    
    def resolve_user(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        id = kwargs.get('id')       
                
        if email and password :            
            user = authenticate(email = email, password=password)
            if user:
                token = create_acces_token({"email": email, "id": id})
                user.save()
                #login(self.request, user)               
                return user
        raise GraphQLError('Email o contraseña incorrectas')


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
                token = create_acces_token({"email": email, "username": username})                 
                user = MyUser.objects.create_user(email=email, password=password, username=username)
                user.save()
                #login(user)
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
    

schema = graphene.Schema(query=Query, mutation=Mutation)