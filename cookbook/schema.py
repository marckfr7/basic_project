import graphene
from ingredients import schema
from user import schemas
import premium.schema


class Query(schema.Query, schemas.Query, premium.schema.Query, graphene.ObjectType):
    pass

class Mutation(schema.Mutation, schemas.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)