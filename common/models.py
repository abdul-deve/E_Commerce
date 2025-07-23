from django.db import models
import  uuid
from .decorators import abstract_model

@abstract_model
class TimeStampUniqueID:
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
