import pytest
import sigmasms


def test_auth_valid_client(requests_mock):
    response = '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "id": "1",' \
               '"username": "username"}'
    requests_mock.post('http://online.sigmasms.ru/api/login', text=response)
    client = sigmasms.Client()
    client.username = 'user'
    client.password = 'pass'
    client.sender = 'sender'
    client._auth()
    assert 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' == client.token


def test_auth_invalid_client(requests_mock):
    response = '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "id": "1",' \
               ' "username": "username"}'
    requests_mock.post('http://online.sigmasms.ru/api/login', text=response)
    client = sigmasms.Client()
    with pytest.raises(ValueError):
        client._auth()


def test_send_message_ok(requests_mock):
    client = sigmasms.Client()
    client.username = 'user'
    client.password = 'pass'
    client.sender = 'sender'
    client.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    response = '{"id": "aca68fa3", "recipient": "+79999999999",' \
               '"status": "pending", "error": null}'
    requests_mock.post('http://online.sigmasms.ru/api/sendings',
                       headers={'Authorization': client.token}, text=response)
    r = client.send_message('+79999999999', 'test', 'sms')
    assert r.json()['error'] is None


def test_send_message_error(requests_mock):
    client = sigmasms.Client()
    client.username = 'user'
    client.password = 'pass'
    client.sender = 'sender'
    client.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    response = '{"id": "aca68fa3", "recipient": "+79999999999",' \
               '"status": "failed", "error": "text"}'
    requests_mock.post('http://online.sigmasms.ru/api/sendings',
                       headers={'Authorization': client.token},
                       text=response)
    r = client.send_message('+79999999999', 'test', 'sms')
    assert 'text' == r.json()['error']


def test_check_status_ok(requests_mock):
    client = sigmasms.Client()
    client.username = 'user'
    client.password = 'pass'
    client.sender = 'sender'
    client.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    _id = "aca68fa3"
    response = '{"id": "aca68fa3", "recipient": "+79999999999",' \
               '"state": {"status": "seen", "error": null}}'
    requests_mock.get('http://online.sigmasms.ru/api/sendings/' + _id,
                      headers={'Authorization': client.token}, text=response)
    r = client.check_status(_id)
    assert r.json()['state']['error'] is None


def test_check_status_error(requests_mock):
    client = sigmasms.Client()
    client.username = 'user'
    client.password = 'pass'
    client.sender = 'sender'
    client.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    _id = "aca68fa3"
    response = '{"id": "aca68fa3", "recipient": "+79999999999",' \
               '"state": {"status": "failed", "error": "text"}}'
    requests_mock.get('http://online.sigmasms.ru/api/sendings/' + _id,
                      headers={'Authorization': client.token}, text=response)
    r = client.check_status(_id)
    assert 'text' == r.json()['state']['error']
