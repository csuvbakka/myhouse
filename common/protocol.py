import json

class Event(object):
    def __init__(self, *args):
        for field in self.fields:
            setattr(self, field, None)

        for field, value in zip(self.fields, args):
            setattr(self, field, value)

    def __repr__(self):
        data = {}
        for field in self.fields:
            data[field] = getattr(self, field)

        return json.dumps(data)

    @classmethod
    def from_json(cls, string):
        data = json.loads(string)
        new_obj = cls()
        for field in cls.fields:
            if field in data:
                value = data[field]
            else:
                value = None
            setattr(new_obj, field, value)

        return new_obj


class Device(Event):
    fields = ['name', 'ip', 'mac', 'status']


class DeviceStatusChange(Event):
    fields = ['device_name', 'user_name', 'new_status']
