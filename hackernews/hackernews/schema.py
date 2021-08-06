import graphene
import graphql_jwt

import links.schema
import users.schema


class Query(users.schema.Query, links.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, links.schema.Mutation, graphene.ObjectType):
    obtainToken = graphql_jwt.ObtainJSONWebToken.Field()
    verifyToken = graphql_jwt.Verify.Field()
    refreshToken = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
