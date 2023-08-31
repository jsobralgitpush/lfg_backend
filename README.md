# Loans For Good - Backend (work in progress)

## Summary
- [Demo](#demo)
- [How to Build the project](#how-to-build-the-project)
- [Project explanation](#project-explanation)
- [EAV explanation](#eav-explanation)
- [Test Coverage](#test-coverage)
- [Code Style](#code-style)
- [References](#references)

## Demo
### Frontend
https://loansforgoodfrontend-06732fd2e7f8.herokuapp.com/

### Django admin
https://loans-for-good-backend-55c8893b4944.herokuapp.com/admin/

## How to build the project
To build the project, you have to download this repo and the [frontend](https://github.com/jsobralgitpush/lfg_frontend_redux) one. After that, create an app tree like this
### App tree
```
(root)
├── loans_for_good_backend
│   ├── (this repo)
├── loans_for_good_frontend
└── docker-compose.yml
```
and use this `docker-compose.yml`, setting the following `config-vars` as your preference or use the current ones from the example (just to test the app)
### env
```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DEBUG=
DATABASE_URL=
REACT_APP_API_HOSTNAME=
REDIS_URL=
```
### docker-compose.yml
```
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword

  backend:
    build:
      context: ./loans_for_good_backend
    command: ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    volumes:
      - ./loans_for_good_backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DEBUG: 'True'
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydatabase
      REDIS_URL: redis://redis:6379/0

  frontend:
    build:
      context: ./loans_for_good_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./loans_for_good_frontend:/app
    environment:
      REACT_APP_API_HOSTNAME: http://localhost:8000
  
  redis:
    image: "redis:latest"
    ports:
      - "6379:6379"
      

  celery:
    build:
      context: ./loans_for_good_backend
    command: celery -A loans_for_good worker --loglevel=info
    volumes:
      - ./loans_for_good_backend:/app
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydatabase
      REDIS_URL: redis://redis:6379/0


volumes:
  postgres_data:

```
### Django admin
Create an `superuser` to access `localhost:8000/admin` panel to create new `Attributes`. To do this, execute:
```
docker ps

# Check the container ID of backend container, in my case above, it's 3a09cf8078cd
CONTAINER ID   IMAGE                  COMMAND                  CREATED        STATUS         PORTS                                                 NAMES
8000889d73da   digital_sys_celery     "celery -A loans_for…"   2 hours ago    Up 6 minutes                                                         digital_sys_celery_1
341acdaf85aa   redis:latest           "docker-entrypoint.s…"   2 hours ago    Up 6 minutes   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp           digital_sys_redis_1
1f99eb2d240c   digital_sys_frontend   "docker-entrypoint.s…"   2 hours ago    Up 6 minutes   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp             digital_sys_frontend_1
3a09cf8078cd   digital_sys_backend    "python manage.py ru…"   2 hours ago    Up 6 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp             digital_sys_backend_1
ad5ed0dc7973   postgres:13            "docker-entrypoint.s…"   30 hours ago   Up 6 minutes   5432/tcp                                              digital_sys_db_1

# open container bash
docker exec -it <container-id> bash

# create super user
python manage.py createsuperuser
```

## Project explanation
The project simulates a financial company which loans money. To request a loan, you have to send a `Proposal`. Users can send, check and refresh the status of all proposals in a SPA. Admin users can register new attributes to proposal and change the status of each proposal.

The project uses an entity called `Proposal` to persist all the proposals send from frontend to backend. The `Proposal` is a model with following attributes:
```
name = models.CharField(max_length=100) -> the name of who is requesting the proposal
document = models.CharField(max_length=20) -> a document from who is requesting the proposal
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_by_system') -> a status for the proposal (the list of available status is set on proposal/model.py
last_updated = models.DateTimeField(auto_now=True) -> the time of last updat on the proposal
```

Besides that, the `Proposal` model is plugged with an `EAV` [entity value attribute](https://inviqa.com/blog/understanding-eav-data-model-and-when-use-it) pattern which makes possible to register new attributes to proposal, like `city`, `address_line`, `state`, `current_job` or whatever. The new attributes registration occurs on `Django Admin` and uses [`django-eav-2`](https://django-eav2.readthedocs.io/en/latest/) lib under the hood. All new attributes registered in `Django Admin` will be sent dinamically to frontend. [Further explanations of how `django-eav2` works will be discuss latter](#eav-explanation).

Finnaly, we'are using an [external API]() to send the proposal fields to our internal system to be 'approved' or 'denied', using a background job for that, plugged in [`Celery`](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) and [`Redis`](https://redis.io/docs/)


## EAV explanation
We choose to use `EAV` pattern since the company needs to register new `attributes` dinamically in the `Django Admin` panel. By the limitations of `ORM` (`Data Integrity`, `Tracebility` and `Consistency`) we cannot do that changing the `schema`. To do so, we are using the `django-eav2` lib which provides a customized solution for it that makes easy to `read`, `create` and `filter` new attributes to a current model

### Create new attributes
```
from eav.models import Attribute

Attribute.objects.create(name='City', slug='city', datatype=Attribute.TYPE_TEXT)
Attribute.objects.create(name='Job Title', slug='job_title', datatype=Attribute.TYPE_TEXT)
```

### Read Values
```
# create a proposal
proposal = Proposal.objects.create(name='Jose', document='123', eav__city='RJ', eav__job_title='Engineer')

# to read a custom attributes registered in Attribute model (like city or job_title)
proposal.eav.city
proposal.eav.job_title

# or
proposal.eav_values.all()
```
### Create Values
```
# as mentioned before
Proposal.objects.create(name='Jose', document='123', eav__city='RJ')

# or
proposal = Proposal.objects.create(name='Jose', document='123')
proposal.eav.city = 'RJ'
proposal.eav.job_title = 'Engineer'
proposal.save()
```

### Filter by Values
```
Proposal.objects.filter(eav__city='RJ')
```

## Test Coverage
To execute the tests, run:
```
coverage run manage.py test
```
To check test coverage:
```
coverage report
```
Full test coverage output:
```
Name                                                Stmts   Miss  Cover
-----------------------------------------------------------------------
loans_for_good/__init__.py                              0      0   100%
loans_for_good/celery.py                                7      0   100%
loans_for_good/settings.py                             30      0   100%
loans_for_good/urls.py                                  3      0   100%
manage.py                                              12      2    83%
proposal/__init__.py                                    0      0   100%
proposal/admin.py                                      17      0   100%
proposal/apps.py                                        4      0   100%
proposal/migrations/0001_initial.py                     5      0   100%
proposal/migrations/0002_proposal_last_updated.py       4      0   100%
proposal/migrations/0003_alter_proposal_status.py       4      0   100%
proposal/migrations/__init__.py                         0      0   100%
proposal/models.py                                      9      0   100%
proposal/serializers.py                                11      0   100%
proposal/services.py                                    5      0   100%
proposal/tasks.py                                      10      0   100%
proposal/tests/__init__.py                              0      0   100%
proposal/tests/test_services.py                        30      1    97%
proposal/tests/test_tasks.py                           32      1    97%
proposal/tests/test_views.py                           36      0   100%
proposal/urls.py                                        4      0   100%
proposal/views.py                                      31      0   100%
-----------------------------------------------------------------------
TOTAL                                                 254      4    98%
```
## Code Style
In this code base we're using the [`PEP8`](https://peps.python.org/pep-0008/) style. We configured a `pre-commit` hooker to prevent us to commit without `PEP8` format. To run autofix, before commits execute:
```
pre-commit run --all-files
```

## References
- [Django for APIs](https://djangoforapis.com/)
- [Django Rest Framwork quickstart](https://realpython.com/django-rest-framework-quick-start/)
- https://github.com/testdrivenio/django-aloe-bdd
