import base64
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.widgets import Widget, ClearableFileInput
from django.template.loader import render_to_string
from datetime import datetime


#class CameraWidget(Widget):
class CameraWidget(ClearableFileInput):
    template = 'webcam/webcam.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'name': name,
            'format': self.attrs['format'],
            'width': self.attrs['width'],
            'height': self.attrs['height'],
            'camera_width': self.attrs['camera_width'],
            'camera_height': self.attrs['camera_height'],
            #'picture': value,
            'url': value and value.url,
            'attrs': attrs,
        })
        #defaults.update(attrs)
        return render_to_string(self.template, context)

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        # proper INPUT FILE html upload either contains either the image, or "false" if the clear checkbox is selected
        # will be "none" if upload is from camera-capture
        if not upload is None:
            return upload
        raw_val = data.get(name, None)
        if raw_val:
            raw_val = raw_val.replace('data:image/jpeg;base64,', '')
            raw_val = raw_val.replace('data:image/png;base64,', '')
        filename = "%s_%s" % (name, datetime.today().isoformat())       # NOTE: not threadsafe

        return SimpleUploadedFile(filename, base64.decodebytes(raw_val.encode()))

        data.name = filename
        data.size = len(raw_val)
        data.raw = raw_val
        return data
        #return filename, raw_val
