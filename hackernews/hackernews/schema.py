import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from links.models import Link
from links.models import Vote


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    postedBy = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Anonymous users can't create links!")
        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            postedBy=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        linkId = graphene.Int()

    def mutate(self, info, linkId):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to vote!")
        link = Link.objects.filter(id=linkId).first()
        if link is None:
            raise Exception(f"The link ={linkId} is invalid.")

        Vote.objects.create(user=user, link=link)

        return CreateVote(user=user, link=link)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    obtainToken = graphql_jwt.ObtainJSONWebToken.Field()
    verifyToken = graphql_jwt.Verify.Field()
    refreshToken = graphql_jwt.Refresh.Field()
    createLink = CreateLink.Field()
    createVote = CreateVote.Field()
    createUser = CreateUser.Field()


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    users = graphene.List(UserType)
    whoami = graphene.Field(UserType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_whoami(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
