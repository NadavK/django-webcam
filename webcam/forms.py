import base64
import uuid
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from webcam.widgets import CameraWidget


#TODO: Consider deriving from ImageField
class CameraField(forms.FileField):
    widget = CameraWidget


    def __init__(self, width=320, height=240, format='jpg',
                 camera_width=320, camera_height=240, *args, **kwargs):
        self.format = format
        self.width = width
        self.height = height
        self.camera_width = camera_width
        self.camera_height = camera_height
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({'width': self.width,
                'height': self.height,
                'format': self.format,
                'camera_width': self.camera_width,
                'camera_height': self.camera_height})
        return attrs
