from django.core.exceptions import ValidationError
import os

def allow_only_image_validators(value):
    ext=os.path.splitext(value.name)[1]
    valid_extentions=['.png','.jpg','.jpeg']
    if not ext.lower in valid_extentions:
        raise ValidationError('unsupported file extention.')