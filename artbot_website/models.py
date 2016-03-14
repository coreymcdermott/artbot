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
    titleRaw    = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image       = models.TextField()
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

            key = self.venue + '-' + self.description.replace(" ", "_") + '-' + self.start.strftime("%y-%m-%d") + '.jpg'
            s3 = boto3.resource('s3')

            try:
                s3.Bucket(os.environ.get('AWS_S3_BUCKET')).put_object(Key = key, Body = image_out.getvalue(), ACL='public-read')
            except:
                raise
            else:
                self.image = 'https://s3-ap-southeast-2.amazonaws.com/artbot.io/' + key
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
