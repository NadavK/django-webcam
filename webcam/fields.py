from django.db import models
from webcam.picture import CameraPicture


class CameraField(models.FileField):
    attr_class = CameraPicture
