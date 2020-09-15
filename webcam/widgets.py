import base64
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.widgets import Widget, ClearableFileInput
from django.template.loader import render_to_string
from datetime import datetime
import re

#class CameraWidget(Widget):
class CameraWidget(ClearableFileInput):
    template = 'webcam/webcam.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'image_id': name + '-image_id',
            'preview_id': name + '-preview_id',
            'camera_id': name + '-camera_id',
            'canvas_id': name + '-canvas_id',
            'take_snapshot_id': name + '-take_snapshot_id',
            'change_snapshot_id': name + '-change_snapshot_id',
            #'url': value.url
        })
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        #template = loader.get_template(self.template_name).render(context)
        return render_to_string(self.template, context)

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        # proper INPUT FILE html upload either contains either the image, or "false" if the clear checkbox is selected
        # will be "none" if upload is from camera-capture
        if not upload is None:
            return upload
        file_formdata  = data.get(name, None)
        if not file_formdata:
            return None

        # data:image/png;base64,{raw data...}
        image_type, image_raw = file_formdata.split(',', 1);    # Extract the meta-data and the raw-data
        image_type = re.search('/(.*);', 'data:image/png;base64').group(1)  # extract jpeg, png, etc.
        filename = "%s_%s.%s" % (name, datetime.today().isoformat(), image_type)       # NOTE: not threadsafe
        try:
            return SimpleUploadedFile(filename, base64.decodebytes(image_raw.encode()))
        except:
            return None
