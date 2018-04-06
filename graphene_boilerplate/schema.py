import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from graphene_boilerplate.ext import db
from graphene_boilerplate.models import Item as ItemModel


class Item(SQLAlchemyObjectType):
    class Meta:
        model = ItemModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_items = SQLAlchemyConnectionField(Item)


class CreateItem(graphene.Mutation):
    class Arguments:
        key = graphene.String()
        value = graphene.JSONString()

    ok = graphene.Boolean()
    item = graphene.Field(lambda: Item)

    def mutate(self, info, key, value):
        item = ItemModel(key=key, value=value)
        db.session.add(item)
        db.session.commit()
        return CreateItem(ok=True, item=item)


class Mutations(graphene.ObjectType):
    create_item = CreateItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
