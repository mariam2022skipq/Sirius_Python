import urllib3

def create_dynamoDB_table():
        table = db_.Table("AlarmTable",
        partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING),
        sort_key=db_.Attribute(name="Timestamp",type=db_.AttributeType.STRING))
        return table

def test_dynamo_existence(stack):
    table=stack.create_dynamoDB_table
    assert table is not None