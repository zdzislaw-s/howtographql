import graphene
from graphene_django import DjangoObjectType

from links.models import Link
from links.models import Vote
from users.schema import UserType


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


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
            raise Exception(f'The link ={linkId} is invalid.')

        Vote.objects.create(user=user, link=link)

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    createLink = CreateLink.Field()
    createVote = CreateVote.Field()
