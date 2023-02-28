import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import MyUser
from .utils import create_acces_token, create_refresh_token


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
            user = MyUser.objects.get(email = email, password=password)
            if user:
                token = create_acces_token({"email": email, "id": id})
                user.save()               
                return user
        return None


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
        ok = True        
        token = create_acces_token({"email": email, "username": username})  
        user_instance = MyUser(username=username, email=email, password=password)
        user_instance.save()
        return CreateMyUser(ok=ok, user = user_instance, token = token)


class UpdateMyUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MyUserInput(required=True)
                
    ok = graphene.Boolean()
    user = graphene.Field(MyUserType)
    
    @staticmethod
    def mutate(root, info, id, input=None):
        user_instance = MyUser.objects.get(pk = id)
        token = token
                
        if user_instance:
            ok = True
            user_instance.username = input.username
            user_instance.email = input.email
            user_instance.password = input.password
            user_instance.save()
            return UpdateMyUser(ok=ok, user = user_instance)
        return UpdateMyUser(ok=False, user = None)



class Mutation(graphene.ObjectType):
    create_my_user = CreateMyUser.Field()
    update_my_user = UpdateMyUser.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)