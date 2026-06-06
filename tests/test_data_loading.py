import json

def test_load_topics():
    with open('data/topics.json') as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) > 0

def test_load_affiliates():
    with open('data/affiliates.json') as f:
        data = json.load(f)
    assert isinstance(data, dict)