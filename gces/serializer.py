# Credits to Abhinav Upadhyay (https://github.com/abhinav-upadhyay)
import json
import datetime
from dateutil.parser import parse

class DateDateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        super(DateDateTimeDecoder, self).__init__(object_hook=self.dict_to_object,
                             *args, **kargs)
    
    def dict_to_object(self, d): 
        if '__type__' not in d:
            return d

        try:
            if d['__type__'] in ['datetime', 'date']:
                dateobj = parse(d['isoformat'])
                type_ = d.pop('__type__')
                return dateobj.date() if type_ == 'date' else dateobj
            else:
                return d
        except:
            return d

class DateDateTimeEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
            return {
                '__type__' : 'datetime',
                'isoformat' : obj.isoformat(),
            }
        elif isinstance(obj, datetime.date):
            return {
                '__type__' : 'date',
                'isoformat' : obj.isoformat(),
            }
        else:
            return json.JSONEncoder.default(self, obj)


def serialize(data):
    return json.dumps(data,cls=DateDateTimeEncoder)


def deserialize(data):
    return json.loads(data, cls=DateDateTimeDecoder)
