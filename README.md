## Artbot

Artbot lists exhibitions open in the coming weekend, automatically scraping data from gallery websites.

Artbot is written in Python and built on [Django](http://scrapy.org) and [Scrapy](http://scrapy.org).

## Supported Galleries

Artbot is currently focused on galleries in Sydney, Australia.

* [aMBUSH Gallery](http://ambushgallery.com/)
* [Art Gallery of NSW](http://www.artgallery.nsw.gov.au)
* [Arthouse Gallery](http://www.arthousegallery.com.au)
* [Firstdraft](http://firstdraft.org.au)
* [Galerie pompom](http://www.galeriepompom.com/)
* [Museum of Contemporary Art Australia](http://www.mca.com.au)
* [UTS ART](http://art.uts.edu.au/)

## Installation

1. Clone this repo.
2. Ensure that the following environmental variables are set:
  * ALLOWED_HOSTS
  * SECRET_KEY
  * DATABASE_URL
  * AWS_ACCESS_KEY_ID
  * AWS_SECRET_ACCESS_KEY
  * AWS_DEFAULT_REGION
  * AWS_S3_BUCKET
3. Run `$ pip install -r requirements.txt`.
4. Run `$ python manage.py collectstatic`.
5. Run `$ python manage.py scrapy crawllall`.
6. Run `$ python manage.py runserver`.

## License

[MIT](https://github.com/coreymcdermott/artbot/blob/fa787806a77f13e5553a5157dbbf179c25f964e9/LICENSE.md) © Corey McDermott
