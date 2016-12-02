## Artbot

I believe that art should be accessible to everyone.

Artbot lists exhibitions open in the coming weekend, automatically scraping data from gallery websites.

Artbot is written in Python and built on [Django](http://scrapy.org) and [Scrapy](http://scrapy.org).

## Supported Galleries

Artbot is currently focused on galleries in Sydney, Australia.

* [4A Centre for Contemporary Asian Art](http://www.4a.com.au/)
* [107 Projects](http://107projects.org/whats-on/?type=exhibition)
* [aMBUSH Gallery](http://ambushgallery.com/)
* [Art Gallery of NSW](http://www.artgallery.nsw.gov.au)
* [Arthouse Gallery](http://www.arthousegallery.com.au)
* [Firstdraft](http://firstdraft.org.au)
* [Galerie pompom](http://www.galeriepompom.com/)
* [m2 Gallery](http://m2gallery.com.au)
* [Mild Manners](http://mild-manners.com/JEDDA-DAISY-CULLEY-UNIVERSAL-LOVE)
* [Museum of Contemporary Art Australia](http://www.mca.com.au)
* [National Art School](http://www.nas.edu.au/NASGallery/Current-Exhibition-and-Events)
* [Sarah Cottier Gallery](http://www.sarahcottiergallery.com/)
* [The Commercial](http://thecommercialgallery.com/)
* [UNSW Galleries](https://www.artdesign.unsw.edu.au/unsw-galleries)
* [UTS ART](http://art.uts.edu.au/)
* [Verge Gallery](https://verge-gallery.net)

## Installation

1. Clone this repo.
2. Ensure that the following environmental variables are set:
  * DEBUG
  * ALLOWED_HOSTS
  * SECRET_KEY
  * DATABASE_URL
  * AWS_ACCESS_KEY_ID
  * AWS_SECRET_ACCESS_KEY
  * AWS_DEFAULT_REGION
  * AWS_S3_BUCKET
  * MAILGUN_SERVER_NAME
  * MAILGUN_ACCESS_KEY
  * SERVER_EMAIL
  * ADMIN_EMAIL
  * LOG_RETENTION
3. Run `$ pip install -r requirements.txt`.
4. Run `$ python manage.py collectstatic`.
5. Run `$ python manage.py crawl all`.
6. Run `$ python manage.py runserver`.

## License

[MIT](https://github.com/coreymcdermott/artbot/blob/fa787806a77f13e5553a5157dbbf179c25f964e9/LICENSE.md) © Corey McDermott
