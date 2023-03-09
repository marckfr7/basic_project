import graphene
from ingredients import schema
from user import schemas
import premium.schema
import graphql_jwt


class Query(schema.Query, schemas.Query, premium.schema.Query, graphene.ObjectType):
    pass

class Mutation(schema.Mutation, schemas.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)