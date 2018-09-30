import json
from django.db import models

class JSONField(models.TextField):
    description = "Json"
    def from_db_value(self,value,expression,connection,content):
        #if value is None:
        #    return value
        try:
            return json.loads(value)
        except Exception:
            return value
    def to_python(self, value):
        try:
            return json.loads(value)
        except:
            pass
        return v
    def get_prep_value(self, value):
        return json.dumps(value)
