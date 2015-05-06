# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from semantria.error import DocumentLengthExceededEror, SemantriaError

class JsonSerializer:
    def gettype(self):
        return "json"

    def serialize(self, obj, wrapper=None):
        if isinstance(obj, dict) and "cloned" in obj:
            if isinstance(obj["cloned"], dict):
                item = obj["cloned"]
                item["template"] = item["config_id"]
                del item["config_id"]
                obj["added"].append(item)
            elif isinstance(obj["cloned"], list):
                for item in obj["cloned"]:
                    item["template"] = item["config_id"]
                    del item["config_id"]
                    obj["added"].append(item)
            else:
                raise SemantriaError('Unsupported object type: %s' % obj)

            del obj["cloned"]

        #encoder = json.JSONEncoder()
        if isinstance(obj, list):
            result = []
            for i in obj:
                seria_i = json.dumps(i)
                if len(seria_i) >= 8192:
                    raise DocumentLengthExceededEror('Document length exceeded. Length: {0}'.format(len(result)))
                result.append(i)
            result = json.dumps(result)
        else:
            result = json.dumps(obj)
            if len(obj) >= 8192:
                    raise DocumentLengthExceededEror('Document length exceeded. Length: {0}'.format(len(result)))

        return result

    def deserialize(self, string, handler=None):
        #decoder = json.JSONDecoder()
        if isinstance(string, bytes):
            return json.loads(string.decode('utf-8'))
        elif isinstance(string, str):
            return json.loads(string)
        else:
            raise RuntimeError("Can't deserialize a {}".format(type(string)))
