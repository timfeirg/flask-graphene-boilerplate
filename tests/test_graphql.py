import json


def dumpdump(s):
    """double json.dumps string"""
    return json.dumps(json.dumps(s))


def test_crud(graphene_client):
    sample_key = 'whatever'
    sample_value = {'foo': 'bar'}
    query = '''
    mutation testCreateItem {
        createItem(key: %s, value: %s) {
            ok
            item {
                key
                value
            }
        }
    }
    ''' % (json.dumps(sample_key), dumpdump(sample_value))
    res = graphene_client.execute(query)
    assert res['data']['createItem']['ok'] is True
    created_item = res['data']['createItem']['item']
    assert created_item['key'] == sample_key
    assert json.loads(created_item['value']) == sample_value
