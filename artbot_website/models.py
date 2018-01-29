import urllib
import boto3
import os
from django.db    import models
from django.utils import timezone
from PIL          import Image, ImageChops
from io           import StringIO


class Event(models.Model):
    DRAFT_STATUS     = 0
    PUBLISHED_STATUS = 1
    HIDDEN_STATUS    = 2

    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Draft'),
        (PUBLISHED_STATUS, 'Published'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    url         = models.TextField()
    venue       = models.TextField()
    title       = models.TextField()
    title_raw   = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image       = models.TextField(blank=True, null=True)
    start       = models.DateTimeField(blank=True, null=True)
    end         = models.DateTimeField(blank=True, null=True)
    created     = models.DateTimeField(auto_now_add=True)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)

    class Meta:
        unique_together = ('venue', 'title_raw')

    def __unicode__(self):
        return self.title

    def crop_image(self):

        try:
            image = Image.open(StringIO(urllib.urlopen(self.image).read()))
        except:
            raise
        else:
            image_out = StringIO()

            border = Image.new(image.mode, image.size, image.getpixel((0, 0)))
            diff   = ImageChops.difference(image, border)
            diff   = ImageChops.add(diff, diff, 2.0, -100)
            bbox   = diff.getbbox()

            if bbox:
                image = image.crop(bbox)
                image.save(image_out, 'JPEG')
            else:
                raise ValueError('Unable to determine image bounding box')

            s3     = boto3.resource('s3')
            region = os.environ.get('AWS_DEFAULT_REGION')
            bucket = s3.Bucket(os.environ.get('AWS_S3_BUCKET'))
            key    = self.venue.replace(" ", "_") + '-' + self.title_raw.replace(" ", "_") + '-' + self.start.strftime("%y-%m-%d") + '.jpg'

            try:
                bucket.put_object(Key = key, Body = image_out.getvalue(), ACL='public-read')
            except:
                raise
            else:
                self.image = 'http://s3-{}.amazonaws.com/{}/{}'.format(region, bucket.name, key)
                self.save()

class Log(models.Model):
    level     = models.TextField()
    message   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SponsoredContent(models.Model):
    DRAFT_STATUS     = 0
    PUBLISHED_STATUS = 1

    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Draft'),
        (PUBLISHED_STATUS, 'Published'),
    )

    url         = models.TextField()
    url_text    = models.TextField()
    sponsor     = models.TextField()
    title       = models.TextField()
    description = models.TextField()
    image       = models.TextField()
    start       = models.DateTimeField(blank=True, null=True)
    end         = models.DateTimeField(blank=True, null=True)
    created     = models.DateTimeField(auto_now_add=True)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)

    class Meta:
        verbose_name = 'Sponsored content'
        verbose_name_plural = 'Sponsored content'
