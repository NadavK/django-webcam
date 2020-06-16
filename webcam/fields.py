import os
from django.db import models
from django.utils.text import capfirst
from webcam import forms
from webcam.picture import CameraPicture


class CameraField(models.FileField):
    attr_class = CameraPicture

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', 'jpg')
        super(CameraField, self).__init__(*args, **kwargs)

    def generate_filename(self, instance, filename):
        filename = filename + '.' + self.format
        return super().generate_filename(instance, filename)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField,
                    'format': self.format,
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        defaults.update(kwargs)
        return super(CameraField, self).formfield(**defaults)
