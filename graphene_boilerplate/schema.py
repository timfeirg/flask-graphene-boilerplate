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


class DeleteItem(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=False)
        key = graphene.String(required=False)

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        item = None
        if not kwargs:
            raise Exception('Must provide either id_ or key')
        if kwargs.get('_id'):
            item = ItemModel.get(kwargs['id_'])
        else:
            item = ItemModel.get_by_key(kwargs['key'])

        if not item:
            raise Exception('Item not found')
        item.delete()
        return DeleteItem(ok=True)


class Mutations(graphene.ObjectType):
    create_item = CreateItem.Field()
    delete_item = DeleteItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
