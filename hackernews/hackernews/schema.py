import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.db.models import Q
from graphql import GraphQLError

from links.models import Link as LinkModel
from links.models import Vote


class Link(DjangoObjectType):
    class Meta:
        model = LinkModel


class Vote(DjangoObjectType):
    class Meta:
        model = Vote


class User(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    postedBy = graphene.Field(User)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Anonymous users can't create links!")
        link = LinkModel(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            postedBy=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(User)
    link = graphene.Field(Link)

    class Arguments:
        linkId = graphene.Int()

    def mutate(self, info, linkId):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to vote!")
        link = LinkModel.objects.filter(id=linkId).first()
        if link is None:
            raise GraphQLError(f"The link ={linkId} is invalid.")

        Vote.objects.create(user=user, link=link)

        return CreateVote(user=user, link=link)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

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
    links = graphene.List(Link, search=graphene.String())
    votes = graphene.List(Vote)
    users = graphene.List(User)
    whoami = graphene.Field(User)

    def resolve_links(self, info, search=None, **kwargs):
        objects = LinkModel.objects
        if search is None:
            return objects.all()
        else:
            filter = Q(url__icontains=search) | Q(description__icontains=search)
            return objects.filter(filter)

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_whoami(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
