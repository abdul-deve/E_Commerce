from django.db import models
import  uuid
def abstract_model(cls):
    class Meta:
        abstract = True

    cls.Meta = type(
        'Meta',
        (getattr(cls, 'Meta', object),),
        {'abstract': True}
    )
    return cls

@abstract_model
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@abstract_model
class UniqueID(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4())

