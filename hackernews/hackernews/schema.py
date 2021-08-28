from graphql import GraphQLError
import graphene

from graphql_jwt import ObtainJSONWebToken as ObtainToken
from graphql_jwt import Verify as VerifyToken
from graphql_jwt import Refresh as RefreshToken
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.db.models import Q

from links.models import Link as LinkModel
from links.models import Vote as VoteModel

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


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

    def mutate(parent, info, url, description):
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

    def mutate(parent, info, linkId):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to vote!")
        link = LinkModel.objects.filter(id=linkId).first()
        if link is None:
            raise GraphQLError(f"The link ={linkId} is invalid.")

        VoteModel.objects.create(user=user, link=link)
        
        rv = CreateVote(user=user, link=link)
        async_to_sync(channel_layer.group_send)("votes", {"data": rv})
        return rv


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(parent, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class SendMessage(graphene.Mutation):
    class Arguments:
        message = graphene.String()

    reply = graphene.String()

    def mutate(self, info, message):
        async_to_sync(channel_layer.group_send)("messages", {"data": message})
        return SendMessage(reply=message)


class Mutation(graphene.ObjectType):
    obtainToken = ObtainToken.Field()
    verifyToken = VerifyToken.Field()
    refreshToken = RefreshToken.Field()
    createLink = CreateLink.Field()
    createVote = CreateVote.Field()
    createUser = CreateUser.Field()
    sendMessage = SendMessage.Field()


class Query(graphene.ObjectType):
    links = graphene.List(
        Link, search=graphene.String(), first=graphene.Int(), skip=graphene.Int()
    )
    votes = graphene.List(Vote)
    users = graphene.List(User)
    whoami = graphene.Field(User)

    def resolve_links(parent, info, search=None, first=None, skip=None, **kwargs):
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

    def resolve_votes(parent, info, **kwargs):
        return VoteModel.objects.all()

    def resolve_users(parent, info):
        return get_user_model().objects.all()

    def resolve_whoami(parent, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user


class Subscription(graphene.ObjectType):
    message = graphene.String()
    vote = graphene.Field(CreateVote)

    async def resolve_message(parent, info):
        channelName = await channel_layer.new_channel()
        await channel_layer.group_add("messages", channelName)
        try:
            while True:
                message = await channel_layer.receive(channelName)
                yield message["data"]
        finally:
            await channel_layer.group_discard("messages", channelName)

    async def resolve_vote(parent, info):
        channelName = await channel_layer.new_channel()
        await channel_layer.group_add("votes", channelName)
        try:
            while True:
                vote = await channel_layer.receive(channelName)
                yield vote["data"]
        finally:
            await channel_layer.group_discard("messages", channelName)


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
