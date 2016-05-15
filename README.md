# resolutions
A resolution typing and exporting system made for use in the European Youth Parliament

Currently being specially built with a few sessions in mind - but soon to be avaliable to all!

## How can I run a local copy of `resolutions`?

To run this web app locally, clone the repository, cd into it and execute the following commands.

`pip install virtualenv`

`virtualenv .`

`source bin/activate`

`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py runserver`

Please note that this is only a development server which should never be used for production scenarios.

You can now login to the [admin area of your local development server](http://localhost:8000/admin/) and start creating sample content.

### Troubleshooting

If you run into problems try installing the dependencies from `requirements.txt` using `pip install -r requirements.txt` but be aware whether you're in a virtual environment or not. We do not want to alter the system's actual environment.
