from django.db    import models
from django.utils import timezone

class Event(models.Model):
    url         = models.TextField()
    venue       = models.TextField()
    title       = models.TextField()
    description = models.TextField()
    image       = models.TextField()
    start       = models.DateTimeField(blank = True, null = True)
    end         = models.DateTimeField(blank = True, null = True)
    created     = models.DateTimeField(default = timezone.now)
    published   = models.BooleanField(default = False)

    class Meta:
        unique_together = ('venue', 'title')

    def __unicode__(self):
        return self.title
