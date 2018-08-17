from .serializer import serialize, deserialize


class Message(object):
    def __init__(self, message):
        self.message = message
        message = deserialize(message.data)
        self.id = self.message.message_id
        self.event = message['event']
        self.data = message.get('data', {})

    def ack(self):
        self.message.ack()

class Event(object):
    def __init__(self, event, data):
        self.body = serialize(
            {
                'event': event,
                'data': data
            }
        ).encode('utf-8')
