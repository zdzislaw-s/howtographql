import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.db.models import Q
from graphql import GraphQLError

from links.models import Link as LinkModel
from links.models import Vote as VoteModel


class Link(DjangoObjectType):
    class Meta:
        model = LinkModel


class Vote(DjangoObjectType):
    class Meta:
        model = VoteModel


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

        VoteModel.objects.create(user=user, link=link)

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
    links = graphene.List(
        Link, search=graphene.String(), first=graphene.Int(), skip=graphene.Int()
    )
    votes = graphene.List(Vote)
    users = graphene.List(User)
    whoami = graphene.Field(User)

    def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
        objects = LinkModel.objects
        qs = []
        if search is None:
            qs = objects.all()
        else:
            filter = Q(url__icontains=search) | Q(description__icontains=search)
            qs = objects.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        return VoteModel.objects.all()

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_whoami(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
