from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):         # pylint: disable=W0223
    location = settings.MEDIAFILES_LOCATION
