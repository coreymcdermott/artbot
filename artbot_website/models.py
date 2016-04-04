import urllib
import boto3
import os
from django.db    import models
from django.utils import timezone
from PIL          import Image, ImageChops
from StringIO     import StringIO


class Event(models.Model):
    url         = models.TextField()
    venue       = models.TextField()
    title       = models.TextField()
    titleRaw    = models.TextField()
    description = models.TextField(blank=True, null=True)
    image       = models.TextField(blank=True, null=True)
    start       = models.DateTimeField(blank=True, null=True)
    end         = models.DateTimeField(blank=True, null=True)
    created     = models.DateTimeField(auto_now_add=True)
    published   = models.BooleanField(default=False)

    class Meta:
        unique_together = ('venue', 'titleRaw')

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
            key    = self.venue.replace(" ", "_") + '-' + self.titleRaw.replace(" ", "_") + '-' + self.start.strftime("%y-%m-%d") + '.jpg'

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

class Sponsor(models.Model):
    url         = models.TextField()
    title       = models.TextField()
    description = models.TextField()
    image       = models.TextField()
    start       = models.DateTimeField()
    end         = models.DateTimeField()
    created     = models.DateTimeField(auto_now_add=True)
    published   = models.BooleanField(default=False)
