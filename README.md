# sigmasms

sigmasms is a module that provides an interface for sigmasms.ru API.

## Usage

```python
from sigmasms import Client

client = Client(username='login', password='password', sender='MessageSender')
send_resp = client.send_message('+79999999999', 'text', 'sms')
print(send_resp.json())

status_resp = client.check_status(send_resp.json()['id'])
print(status_resp.json())

```

## Changelog

0.1.0 - Release module
