# -*- coding: utf-8 -*-

import pytest
from graphene.test import Client as GrapheneClient
from urllib.parse import urlparse

from graphene_boilerplate.app import create_app
from graphene_boilerplate.ext import db
from graphene_boilerplate.schema import schema


json_headers = {'Content-Type': 'application/json'}


@pytest.fixture
def app(request):
    app = create_app()
    app.config['DEBUG'] = True

    ctx = app.app_context()
    ctx.push()

    def tear_down():
        ctx.pop()

    request.addfinalizer(tear_down)
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_db(request, app):

    def check_service_host(uri):
        """只能在本地或者容器里跑测试"""
        u = urlparse(uri)
        return u.hostname in ('localhost', '127.0.0.1') or 'hub.ricebook.net__ci__' in u.hostname

    if not check_service_host(app.config['SQLALCHEMY_DATABASE_URI']):
        raise Exception('Need to run test on localhost or in container')

    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture
def graphene_client(test_db):
    return GrapheneClient(schema)
