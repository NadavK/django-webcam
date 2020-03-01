from django.forms.widgets import Widget
from django.template.loader import render_to_string


class CameraWidget(Widget):
    template = 'webcam/webcam.html'

    def render(self, name, value, attrs=None, renderer=None):
        defaults = {'name': name,
                    'format': self.attrs['format'],
                    'width': self.attrs['width'],
                    'height': self.attrs['height'],
                    'camera_width': self.attrs['camera_width'],
                    'camera_height': self.attrs['camera_height'],
                    'picture': value,
                    'attrs': attrs}
        defaults.update(attrs)
        return render_to_string(self.template, defaults)

    def value_from_datadict(self, data, files, name):
        raw_val = data.get("data_%s" % name, None)
        filename = data.get("%s" % name, None)
        if raw_val:
            raw_val = raw_val.replace('data:image/jpeg;base64,', '')
        return filename, raw_val
