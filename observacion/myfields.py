# Custom Fields
from settings import DATABASE_ENGINE
from django.db import models

class DateTimeField(models.DateTimeField):
    def db_type(self):
        if DATABASE_ENGINE == 'postgresql_psycopg2':
            return "timestamp without time zone"
        else:
            return super(DateTimeField, self).db_type()
        #super(DateTimeField, self).__init__(*args, **kwargs)

class BigAutoField(models.AutoField):
    empty_strings_allowed=False

    def get_internal_type(self):
        return "BigIntegerField"

    def db_type(self):
        if DATABASE_ENGINE == 'mysql':
            return 'bigint zerofill auto_increment'
        else:
            return 'bigserial'

class BigIntegerField(models.IntegerField):
    empty_strings_allowed=False

    def get_internal_type(self):
        return "BigIntegerField"

    def db_type(self):
        return 'bigint'

class ForeignKey(models.ForeignKey):
    def db_type(self):
        rel_field = self.rel.get_related_field()
        if (isinstance(rel_field, BigAutoField)):
            return BigIntegerField().db_type()
        super(ForeignKey, self).db_type(self)

  