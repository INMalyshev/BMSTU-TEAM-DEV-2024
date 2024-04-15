from cards import ping


def test_ping():
    assert ping() == 'pong'
